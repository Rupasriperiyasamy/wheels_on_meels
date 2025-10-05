#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import sys, cgitb, pymysql, os, http.cookies, cgi

sys.stdout.reconfigure(encoding='utf-8')
cgitb.enable(display=1)

print("Content-type:text/html\r\n\r\n")

# HTML Header
html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Checkout</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<style>
body {
    background-color: #f8f9fa;
    padding: 20px;
}
.checkout-card {
    max-width: 500px;
    margin: 30px auto;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    background: #fff;
}
h2 {
    text-align: center;
    margin-bottom: 20px;
    font-weight: 600;
}
.alert-box {
    text-align: center;
    margin-bottom: 20px;
}
.btn-custom {
    width: 100%;
    margin-top: 10px;
}
.cart-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #dee2e6;
}
.cart-item:last-child {
    border-bottom: none;
}
</style>
</head>
<body>
<div class="checkout-card">
"""

html_footer = "</div></body></html>"

print(html_header)

# 1️⃣ Check login cookie
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
if "user" not in cookie:
    print("<div class='alert alert-warning alert-box'>Please <a href='login_user.py'>login</a> first.</div>")
    print(html_footer)
    exit()

user_email = cookie["user"].value.strip()

# 2️⃣ Get form data
form = cgi.FieldStorage()
payment_method = form.getvalue("payment_method", "").strip()

# 3️⃣ Connect to database
try:
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="wheelsonmeals",
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = con.cursor()
except Exception as e:
    print(f"<div class='alert alert-danger alert-box'>Database connection error: {e}</div>")
    print(html_footer)
    exit()

try:
    # 4️⃣ Get user ID
    cur.execute("SELECT id FROM user_register WHERE email=%s", (user_email,))
    user_row = cur.fetchone()
    if not user_row:
        print("<div class='alert alert-danger alert-box'>User not found. <a href='login_user.py'>Login</a></div>")
        print(html_footer)
        exit()
    user_id = user_row['id']

    # 5️⃣ Fetch cart items
    cur.execute("""
        SELECT c.product_id, p.name, p.price, c.quantity
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id=%s
    """, (user_id,))
    cart_items = cur.fetchall()

    if not cart_items:
        print("<div class='alert alert-info alert-box'>Your cart is empty. <a href='home.py'>Shop Now</a></div>")
        print(html_footer)
        exit()

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    # 6️⃣ Payment processing
    if payment_method:
        cur.execute("INSERT INTO orders (user_id, total_amount) VALUES (%s, %s)", (user_id, total))
        order_id = cur.lastrowid

        cur.execute("INSERT INTO payment (order_id, amount, payment_method) VALUES (%s, %s, %s)",
                    (order_id, total, payment_method))

        cur.execute("DELETE FROM cart WHERE user_id=%s", (user_id,))
        con.commit()

        # Success message
        print(f"""
        <div class='alert alert-success alert-box'>
            ✅ Payment Successful!<br>
            <strong>Order ID:</strong> {order_id}<br>
            <strong>Total:</strong> ₹{total:.2f}<br>
            <strong>Payment Method:</strong> {payment_method}
        </div>
        <a href='home.py' class='btn btn-primary btn-custom'>Go to Home</a>
        <a href='cart.py' class='btn btn-success btn-custom'>View Cart</a>
        """)
    else:
        # Show payment form
        print(f"""
        <h2>Checkout</h2>
        <div class='alert alert-info alert-box'>
            <strong>Total Amount:</strong> ₹{total:.2f}
        </div>

        <div class="mb-3">
            <h5>Items in Cart</h5>
            <div class="border rounded p-2 mb-3">
        """)
        for item in cart_items:
            print(f"<div class='cart-item'><span>{item['name']} x {item['quantity']}</span><span>₹{item['price']*item['quantity']:.2f}</span></div>")

        print(f"""
            </div>
        </div>

        <form method='post'>
            <div class="mb-3">
                <label for="payment_method" class="form-label">Payment Method:</label>
                <select name='payment_method' id="payment_method" class="form-select" required>
                    <option value='Credit Card'>Credit Card</option>
                    <option value='Debit Card'>Debit Card</option>
                    <option value='UPI'>UPI</option>
                    <option value='Cash on Delivery'>Cash on Delivery</option>
                </select>
            </div>
            <button type='submit' class='btn btn-success btn-custom'>Pay Now</button>
        </form>
        <a href='cart.py' class='btn btn-secondary btn-custom mt-2'>Back to Cart</a>
        """)

except pymysql.MySQLError as e:
    print(f"<div class='alert alert-danger alert-box'>Database error: {e}</div>")

finally:
    cur.close()
    con.close()
    print(html_footer)
