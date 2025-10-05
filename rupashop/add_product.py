#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import cgi
import cgitb
import os
import pymysql
import http.cookies

cgitb.enable(display=1)  # Show errors in browser

print("Content-type:text/html\r\n\r\n")

# Check admin login via cookie
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
if "admin" not in cookie:
    print("<html><body>Please login <a href='admin_login.py'>here</a></body></html>")
    exit()

# Get form data
form = cgi.FieldStorage()
name = form.getvalue("name", "").strip()
desc = form.getvalue("description", "").strip()
price = form.getvalue("price", "").strip()
image = form.getvalue("image", "").strip()

# Database connection
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="wheelsonmeals"
)
cur = con.cursor()

# If all fields are filled, insert product
if name and desc and price and image:
    try:
        cur.execute(
            "INSERT INTO products (name, description, price, image) VALUES (%s, %s, %s, %s)",
            (name, desc, price, image)
        )
        con.commit()
        print("""
        <html><body>
        <h2>Product added successfully!</h2>
        <a href='admin_page.py'>Back to Dashboard</a>
        </body></html>
        """)
    except pymysql.MySQLError as e:
        print(f"<html><body>Error adding product: {e}<br><a href='add_product.py'>Try again</a></body></html>")
else:
    # Show Add Product form
    print("""
    <html>
    <body>
        <h2>Add Product</h2>
        <form method="post">
            Name: <input type="text" name="name"><br>
            Description: <input type="text" name="description"><br>
            Price: <input type="text" name="price"><br>
            Image Path: <input type="text" name="image"><br>
            <input type="submit" value="Add">
        </form>
        <a href='admin_page.py'>Back to Dashboard</a>
    </body>
    </html>
    """)

# Close connection
cur.close()
con.close()
