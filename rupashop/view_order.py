#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe
import cgitb, pymysql

cgitb.enable()

print("Content-type: text/html\r\n\r\n")

# Connect to DB
con = pymysql.connect(host="localhost", user="root", password="", database="wheelsonmeals")
cur = con.cursor(pymysql.cursors.DictCursor)

try:
    cur.execute("SELECT * FROM order_details ORDER BY order_id DESC")
    orders = cur.fetchall()

    print("<h3>All Orders</h3>")
    print(
        "<table border='1' cellpadding='5'><tr><th>ID</th><th>User Email</th><th>Total Price</th><th>Payment Method</th><th>Order Date</th></tr>")

    if orders:
        for order in orders:
            print(
                f"<tr><td>{order['order_id']}</td><td>{order['user_email']}</td><td>₹{order['total_price']}</td><td>{order['payment_method']}</td><td>{order['order_date']}</td></tr>")
    else:
        print("<tr><td colspan='5'>No orders found.</td></tr>")

    print("</table>")
except Exception as e:
    print(f"<h3 style='color:red;'>Error loading orders: {e}</h3>")
finally:
    con.close()
