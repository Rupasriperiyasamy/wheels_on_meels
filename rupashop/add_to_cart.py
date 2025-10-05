#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import sys, cgi, cgitb, pymysql, http.cookies, os
sys.stdout.reconfigure(encoding='utf-8')
cgitb.enable(display=1)

print("Content-type: text/html\r\n\r\n")

# HTML header
html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Add to Cart</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body class="bg-light">
<div class="container py-5">
"""
html_footer = "</div></body></html>"
print(html_header)

# 1️⃣ Check cookie for logged-in user
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
if "user" not in cookie:
    print("<div class='alert alert-warning'>Please <a href='login_user.py'>login</a> first.</div>")
    print(html_footer)
    exit()

user_email = cookie["user"].value.strip()
print(f"<pre>DEBUG cookie email: {user_email}</pre>")

# 2️⃣ Get product_id from query string
form = cgi.FieldStorage()
product_id = form.getvalue("product_id")
if not product_id:
    print("<div class='alert alert-danger'>Invalid product. <a href='index.py'>Go back</a></div>")
    print(html_footer)
    exit()

# Ensure product_id is integer
try:
    product_id = int(product_id)
except ValueError:
    print("<div class='alert alert-danger'>Invalid product ID format. <a href='index.py'>Go back</a></div>")
    print(html_footer)
    exit()

# 3️⃣ Connect to the database
con = pymysql.connect(host="localhost", user="root", password="", database="wheelsonmeals", cursorclass=pymysql.cursors.DictCursor)
cur = con.cursor()

try:
    # 4️⃣ Validate user exists
    cur.execute("SELECT id FROM user_register WHERE email=%s", (user_email,))
    user_row = cur.fetchone()
    if not user_row:
        print("<div class='alert alert-danger'>User not found. Please register first.</div>")
        print(html_footer)
        exit()
    user_id = int(user_row['id'])
    print(f"<pre>DEBUG user_id: {user_id}</pre>")

    # 5️⃣ Validate product exists
    cur.execute("SELECT id, name, price FROM products WHERE id=%s", (product_id,))
    product = cur.fetchone()
    if not product:
        print(f"<div class='alert alert-danger'>Product with ID {product_id} not found.</div>")
        print(html_footer)
        exit()

    product_name = product['name']
    product_price = product['price']
    print(f"<pre>DEBUG product: {product}</pre>")

    # 6️⃣ Insert into cart or increment quantity if already exists
    try:
        cur.execute("SELECT quantity FROM cart WHERE user_id=%s AND product_id=%s", (user_id, product_id))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id=%s AND product_id=%s", (user_id, product_id))
            action = "incremented"
        else:
            cur.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (%s,%s,1)", (user_id, product_id))
            action = "added"
        con.commit()
        print(f"<pre>DEBUG cart action: {action}</pre>")
    except pymysql.MySQLError as e:
        print(f"<div class='alert alert-danger'>SQL ERROR: {e}</div>")
        print(html_footer)
        exit()

    # 7️⃣ Show Bootstrap modal
    modal_html = f"""
    <button type="button" class="btn btn-primary d-none" id="openModalBtn" data-bs-toggle="modal" data-bs-target="#successModal"></button>

    <div class="modal fade" id="successModal" tabindex="-1" aria-labelledby="successModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title" id="successModalLabel">Product {action}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            ✅ <strong>{product_name}</strong> has been {action} to your cart!<br>
            Price: ₹{product_price}
          </div>
          <div class="modal-footer">
            <a href='home.py' class='btn btn-primary'>Continue Shopping</a>
            <a href='cart.py' class='btn btn-success'>View Cart</a>
          </div>
        </div>
      </div>
    </div>

    <script>
    window.onload = function() {{
        document.getElementById('openModalBtn').click();
    }};
    </script>
    """
    print(modal_html)

finally:
    cur.close()
    con.close()
    print(html_footer)
