#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import sys, cgitb, pymysql, cgi, http.cookies, os
sys.stdout.reconfigure(encoding='utf-8')
cgitb.enable(display=1)

print("Content-type:text/html\r\n\r\n")

# Check user login
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
user_email = cookie["user"].value if "user" in cookie else None

# Get product ID
form = cgi.FieldStorage()
product_id = form.getvalue("id")
if not product_id:
    print("<html><body>No product selected. <a href='home.py'>Go back to Home</a></body></html>")
    exit()

# Connect to database
con = pymysql.connect(host="localhost", user="root", password="", database="wheelsonmeals", cursorclass=pymysql.cursors.DictCursor)
cur = con.cursor()

# Fetch main product details
cur.execute("SELECT id, name, description, price, image FROM products WHERE id=%s", (product_id,))
product = cur.fetchone()
if not product:
    print("<html><body>Product not found. <a href='home.py'>Go back to Home</a></body></html>")
    exit()

# Set correct image path
img_path = product['image'] if product['image'].startswith("uploads/") else f"uploads/{product['image']}"
name, desc, price = product['name'], product['description'], product['price']

# HTML Header
print(f"""
<html>
<head>
    <title>{name} - Product Details</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .related-card img {{
            width: 100%;
            height: 120px;
            object-fit: cover;
            border-radius: 5px;
        }}
        .related-container {{
            gap: 15px;
            scroll-behavior: smooth;
        }}
        .arrow-btn {{
            z-index: 2;
            top: 50%;
            transform: translateY(-50%);
        }}
    </style>
</head>
<body class="bg-light">

<div class="container py-4">
<h2 class="text-center mb-4">{name}</h2>

<div class="row justify-content-center mb-4">
    <div class="col-md-6">
        <div class="card shadow-sm">
            <img src="{img_path}" class="card-img-top" alt="{name}" style="width:100%; height:300px; object-fit:cover; border-radius:5px;">
            <div class="card-body text-center">
                <p class="card-text">{desc}</p>
                <h5 class="text-danger">&#8377;{price}</h5>
                <div class="d-flex justify-content-center mt-3">
                    <a class="btn btn-secondary me-2" href="index.py">Back to Home</a>
""")

if user_email:
    print(f'<a class="btn btn-primary" href="add_to_cart.py?product_id={product_id}&product_name={name}&price={price}">Add to Cart</a>')
else:
    print('<small class="text-muted">Please <a href="login_user.py">login</a> to add to cart</small>')

print("""
                </div>
            </div>
        </div>
    </div>
</div>
""")

# Fetch 10 related products excluding current
cur.execute("SELECT id, name, price, image FROM products WHERE id != %s ORDER BY RAND() LIMIT 10", (product_id,))
related = cur.fetchall()

if related:
    print('<h3 class="text-center mb-3">Related Products</h3>')
    print("""
    <div class="position-relative mb-5">
        <!-- Left Arrow -->
        <button class="btn btn-danger position-absolute start-0 arrow-btn" onclick="scrollLeft()">&lt;</button>

        <!-- Scrollable container -->
        <div id="relatedProducts" class="d-flex overflow-auto related-container">
    """)

    for p in related:
        pid, pname, pprice = p['id'], p['name'], p['price']
        # Set correct path for related product image
        pimg_path = p['image'] if p['image'].startswith("uploads/") else f"uploads/{p['image']}"
        print(f"""
        <div class="card related-card h-100 shadow-sm" style="min-width:180px; flex-shrink:0;">
            <img src="{pimg_path}" alt="{pname}">
            <div class="card-body text-center">
                <h6 class="card-title">{pname}</h6>
                <p class="fw-bold text-danger">&#8377;{pprice}</p>
                <a class="btn btn-success btn-sm me-1 mb-1" href="view_product.py?id={pid}">View</a>
        """)
        if user_email:
            print(f'<a class="btn btn-primary btn-sm mb-1" href="add_to_cart.py?product_id={pid}&product_name={pname}&price={pprice}">Add</a>')
        print("""
            </div>
        </div>
        """)

    print("""
        </div> <!-- scroll container -->
        <!-- Right Arrow -->
        <button class="btn btn-danger position-absolute end-0 arrow-btn" onclick="scrollRight()">&gt;</button>
    </div>
    """)

    # Infinite scroll JS
    print("""
    <script>
    const container = document.getElementById('relatedProducts');
    const scrollAmount = 200;

    function scrollLeft() {
        if(container.scrollLeft === 0){
            container.scrollLeft = container.scrollWidth;
        } else {
            container.scrollBy({left: -scrollAmount, behavior: 'smooth'});
        }
    }

    function scrollRight() {
        if(container.scrollLeft + container.clientWidth >= container.scrollWidth){
            container.scrollLeft = 0;
        } else {
            container.scrollBy({left: scrollAmount, behavior: 'smooth'});
        }
    }
    </script>
    """)

# Footer
print("""
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

cur.close()
con.close()
