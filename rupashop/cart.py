#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import sys, cgi, cgitb, pymysql, http.cookies, os
sys.stdout.reconfigure(encoding='utf-8')
cgitb.enable(display=1)

print("Content-type: text/html; charset=utf-8\r\n\r\n")

# HTML Header
html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Your Cart</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body class="bg-light">
<div class="container py-5">
<h2 class="mb-4">Your Shopping Cart</h2>
"""
html_footer = "</div></body></html>"
print(html_header)

# Check logged-in user
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
if "user" not in cookie:
    print("<div class='alert alert-warning'>Please <a href='login_user.py'>login</a> first.</div>")
    print(html_footer)
    exit()
user_email = cookie["user"].value.strip()

# Connect to database
con = pymysql.connect(host="localhost", user="root", password="", database="wheelsonmeals", cursorclass=pymysql.cursors.DictCursor)
cur = con.cursor()

try:
    # Get user_id
    cur.execute("SELECT id FROM user_register WHERE email=%s", (user_email,))
    user_row = cur.fetchone()
    if not user_row:
        print("<div class='alert alert-danger'>User not found. Please login first.</div>")
        print(html_footer)
        exit()
    user_id = int(user_row['id'])

    # Get cart items
    cur.execute("""
        SELECT c.id AS cart_id, p.name, p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """, (user_id,))
    items = cur.fetchall()

    if not items:
        print("<div class='alert alert-info'>Your cart is empty. <a href='index.py'>Go shopping</a></div>")
        print(html_footer)
        exit()

    # Display cart table
    print("""
    <table class="table table-striped table-bordered">
    <thead class="table-dark">
    <tr>
        <th>Product</th>
        <th>Price</th>
        <th>Quantity</th>
        <th>Total</th>
        <th style="text-align:center;">Action</th>
    </tr>
    </thead>
    <tbody>
    """)

    grand_total = 0
    for item in items:
        total = item['price'] * item['quantity']
        grand_total += total

        increment_link = f"update_cart.py?cart_id={item['cart_id']}&action=increment"
        decrement_link = f"update_cart.py?cart_id={item['cart_id']}&action=decrement"
        remove_link = f"update_cart.py?cart_id={item['cart_id']}&action=remove"

        print(f"""
        <tr>
            <td>{item['name']}</td>
            <td>&#8377;{item['price']}</td>
            <td>{item['quantity']}</td>
            <td>&#8377;{total}</td>
            <td style="text-align:center; font-size:18px;">
                <a href='{increment_link}' style="text-decoration:none; color:green; margin:0 5px;">&#43;</a>
                <a href='{decrement_link}' style="text-decoration:none; color:orange; margin:0 5px;">&#8722;</a>
                <a href='{remove_link}' style="text-decoration:none; color:red; margin:0 5px;">&#10005;</a>
            </td>
        </tr>
        """)

    # Grand total row
    print(f"""
    <tr class='table-success'>
        <td colspan='3'><strong>Grand Total</strong></td>
        <td>&#8377;{grand_total}</td>
        <td></td>
    </tr>
    </tbody>
    </table>

    <a href='home.py' class='btn btn-primary'>Continue Shopping</a>
    <a href='checkout.py' class='btn btn-success'>Checkout</a>
    """)

finally:
    cur.close()
    con.close()
    print(html_footer)
