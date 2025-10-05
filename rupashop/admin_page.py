#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import cgitb, http.cookies, os, pymysql, cgi, shutil, sys

sys.stdout.reconfigure(encoding='utf-8')
cgitb.enable(display=1)

form = cgi.FieldStorage()
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
admin_user = cookie["admin"].value if "admin" in cookie else None

if not admin_user:
    print("Content-type: text/html\r\n\r\n")
    print("<html><body>Please <a href='admin_login.py'>login</a> first.</body></html>")
    exit()

# Database connection
con = pymysql.connect(host="localhost", user="root", password="", database="wheelsonmeals")
cur = con.cursor()

UPLOAD_DIR = "uploads"
WEB_UPLOAD_DIR = "/wheelsonmeals/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ----------------- Handle form submission -----------------
message = ""
if form.getvalue("submit"):
    name = form.getvalue("name", "").strip()
    description = form.getvalue("description", "").strip()
    price = form.getvalue("price", "").strip()

    img_filename = None
    if "image" in form:
        fileitem = form["image"]
        if fileitem.filename:
            img_filename = os.path.basename(fileitem.filename)
            filepath = os.path.join(UPLOAD_DIR, img_filename)
            with open(filepath, "wb") as f:
                shutil.copyfileobj(fileitem.file, f)

    if name and price:
        try:
            cur.execute(
                "INSERT INTO products (name, description, price, image) VALUES (%s,%s,%s,%s)",
                (name, description, price, img_filename)
            )
            con.commit()
            print("Status: 303 See Other")
            print("Location: admin_page.py?msg=success")
            print("\r\n")
            exit()
        except Exception as e:
            message = f"Error adding product: {e}"
    else:
        message = "Please provide both Name and Price."
else:
    msg = form.getvalue("msg")
    message = "Product added successfully!" if msg == "success" else ""

# ----------------- Fetch products -----------------
cur.execute("SELECT id, name, description, price, image FROM products ORDER BY id DESC")
products = cur.fetchall()

# ----------------- Fetch orders -----------------
cur.execute("""
SELECT o.id, u.email, o.total_amount,
       DATE_FORMAT(o.created_at, '%d-%b-%Y %I:%i %p') AS order_time,
       o.status
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
ORDER BY o.created_at DESC
""")
orders = cur.fetchall()

# ----------------- Output HTML -----------------
print("Content-type: text/html; charset=utf-8\r\n\r\n")
print(f"""
<html>
<head>
    <title>Admin Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ background-color: #f8f9fa; padding: 20px; }}
        .container {{ max-width: 1200px; }}
        img {{ max-width: 60px; border-radius: 8px; }}
        a img:hover {{ transform: scale(1.1); transition: 0.3s; }}
        .card {{ margin-bottom: 30px; border-radius: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        th {{ background-color: #343a40; color: white; }}
        .badge-delivered {{ background-color: #28a745; }}
        .badge-pending {{ background-color: #ffc107; color: black; }}
    </style>
</head>
<body>
<div class='container'>
    <h2 class='text-center mb-4'>Welcome Admin: {admin_user}</h2>
    <div class='text-end mb-3'><a href='admin_logout.py' class='btn btn-danger btn-sm'>Logout</a></div>

    <div class='card p-4'>
        <h4>Add New Product</h4>
""")

if message:
    color_class = "text-success" if "successfully" in message else "text-danger"
    print(f"<p class='{color_class}'>{message}</p>")

print("""
        <form method='post' enctype='multipart/form-data' class='row g-3'>
            <div class='col-md-4'>
                <input type='text' name='name' placeholder='Product Name' class='form-control' required>
            </div>
            <div class='col-md-4'>
                <input type='text' name='description' placeholder='Description' class='form-control'>
            </div>
            <div class='col-md-2'>
                <input type='number' step='0.01' name='price' placeholder='Price' class='form-control' required>
            </div>
            <div class='col-md-2'>
                <input type='file' name='image' class='form-control'>
            </div>
            <div class='col-md-12 text-center'>
                <input type='submit' name='submit' value='Add Product' class='btn btn-primary'>
            </div>
        </form>
    </div>

    <div class='card p-4'>
        <h4>Products</h4>
        <table class='table table-striped table-bordered'>
            <tr><th>ID</th><th>Name</th><th>Description</th><th>Price</th><th>Image</th><th>Action</th></tr>
""")

for pid, name, desc, price, img in products:
    img_url = f"{WEB_UPLOAD_DIR}/{img}" if img else "https://via.placeholder.com/50"
    img_tag = f"<a href='view_product.py?id={pid}' target='_blank'><img src='{img_url}' alt='{name}'></a>"
    print(
        f"<tr><td>{pid}</td><td>{name}</td><td>{desc}</td><td>&#8377;{price}</td><td>{img_tag}</td><td><a href='view_product.py?id={pid}' class='btn btn-sm btn-info'>View</a></td></tr>")

print("""
        </table>
    </div>

    <div class='card p-4'>
        <h4>Orders</h4>
""")

if not orders:
    print("<p class='text-danger'>No orders found in the database.</p>")
else:
    print("""
    <table class='table table-striped table-bordered'>
        <tr><th>Order ID</th><th>User Email</th><th>Total</th><th>Time</th><th>Status</th><th>Action</th></tr>
    """)

    for oid, email, total, time, status in orders:
        email_display = email if email else "<span class='text-danger'>Unknown User</span>"
        badge_class = "badge-delivered" if status and status.lower() == "delivered" else "badge-pending"
        status_display = status if status else "Pending"
        print(
            f"<tr><td>{oid}</td><td>{email_display}</td><td>&#8377;{total}</td><td>{time}</td><td><span class='badge {badge_class}'>{status_display}</span></td><td><a href='view_order.py?id={oid}' class='btn btn-sm btn-primary'>View</a></td></tr>")

    print("</table>")

print("""
</div>
</div>
</body>
</html>
""")

cur.close()
con.close()
