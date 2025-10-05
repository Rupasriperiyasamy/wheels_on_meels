#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import cgitb, http.cookies, os, pymysql
import sys
sys.stdout.reconfigure(encoding='utf-8')
cgitb.enable(display=1)

print("Content-type: text/html\r\n\r\n")

# ----------------- Cookie check -----------------
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
user_email = cookie["user"].value if "user" in cookie else None

if not user_email:
    print("<html><body>Please <a href='login_user.py'>login</a> first.</body></html>")
    exit()

# ----------------- Database connection -----------------
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="wheelsonmeals",
    cursorclass=pymysql.cursors.DictCursor
)
cur = con.cursor()

# ----------------- Get user info -----------------
cur.execute("SELECT id, full_name FROM user_register WHERE email=%s", (user_email,))
user = cur.fetchone()

if not user:
    print("<html><body>User not found.</body></html>")
    exit()

user_id = int(user["id"])  # ensure integer

# ----------------- Fetch orders for this user -----------------
query_orders = """
SELECT o.id AS order_id, o.total_amount, o.status,
       DATE_FORMAT(o.created_at, '%%d-%%b-%%Y %%I:%%i %%p') AS order_time
FROM orders o
WHERE o.user_id = %s
ORDER BY o.created_at DESC
"""
cur.execute(query_orders, (user_id,))
orders = cur.fetchall()

# ----------------- HTML Output -----------------
print(f"""
<html>
<head>
    <meta charset='UTF-8'>
    <title>My Orders</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
</head>
<body class="bg-light">
<div class="container mt-5">
    <h2 class="text-center mb-4">My Orders</h2>
    <p class="text-center">Hello, {user['full_name']}!</p>
    <a href="home.py" class="btn btn-primary mb-3"><i class="fas fa-home"></i> Back to Home</a>
""")

if not orders:
    print("<p class='text-center text-danger'>You have no orders yet.</p>")
else:
    print("""
    <table class="table table-striped table-bordered">
        <thead class="table-dark">
            <tr>
                <th>Order ID</th>
                <th>Total Amount</th>
                <th>Status</th>
                <th>Order Time</th>
                <th>Products</th>
            </tr>
        </thead>
        <tbody>
    """)
    for o in orders:
        # Fetch products for each order
        cur.execute("""
        SELECT p.name, op.quantity, p.price
        FROM order_products op
        JOIN products p ON op.product_id = p.id
        WHERE op.order_id = %s
        """, (o['order_id'],))
        products = cur.fetchall()

        # Format product list
        product_list = "<ul>"
        for prod in products:
            product_list += f"<li>{prod['name']} x {prod['quantity']} (₹{prod['price']})</li>"
        product_list += "</ul>"

        # Color code status
        status_color = (
            "text-warning" if o['status'].lower() == "pending"
            else "text-success" if o['status'].lower() == "delivered"
            else "text-danger"
        )

        print(f"<tr><td>{o['order_id']}</td><td>₹{o['total_amount']}</td><td class='{status_color}'>{o['status']}</td><td>{o['order_time']}</td><td>{product_list}</td></tr>")

    print("</tbody></table>")

print("""
</div>
</body>
</html>
""")

cur.close()
con.close()
