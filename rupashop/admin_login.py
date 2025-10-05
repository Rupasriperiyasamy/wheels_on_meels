#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import sys
import io
import cgi
import cgitb
import pymysql
import http.cookies
import hashlib
from pymysql.cursors import DictCursor

# UTF-8 output for CGI
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Enable CGI traceback for debugging
cgitb.enable(display=1)

# Database connection
try:
    con = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="wheelsonmeals",
        cursorclass=DictCursor
    )
    cur = con.cursor()
except Exception as e:
    print("Content-type:text/html\r\n\r\n")
    print(f"<h3>Database connection failed: {e}</h3>")
    sys.exit(0)


def invalid_login():
    """Display invalid login message."""
    print("Content-type:text/html\r\n\r\n")
    print(html_header)
    print(
        "<div class='alert alert-danger text-center'>Invalid username or password ❌</div>"
    )
    print(
        "<a href='admin_login.py' class='btn btn-secondary btn-custom mt-2'>Try Again</a>"
    )
    print(html_footer)


def show_login_form():
    """Display login form."""
    print("Content-type:text/html\r\n\r\n")
    print(html_header)
    print(
        """
    <form method='post'>
        <div class="mb-3">
            <label class="form-label">Username</label>
            <input type='text' name='username' class="form-control" required>
        </div>
        <div class="mb-3">
            <label class="form-label">Password</label>
            <input type='password' name='password' class="form-control" required>
        </div>
        <button type='submit' class='btn btn-primary btn-custom'>Login</button>
    </form>
    """
    )
    print(html_footer)


# HTML header and footer
html_header = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Admin Login</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body { background: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
.card { background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.2); width: 400px; }
h2 { text-align: center; margin-bottom: 25px; }
.btn-custom { width: 100%; }
</style>
</head>
<body>
<div class="card">
<h2>Admin Login</h2>
"""
html_footer = "</div></body></html>"

# Get form data
form = cgi.FieldStorage()
username = form.getvalue("username", "").strip()
password = form.getvalue("password", "").strip()

# Handle login
if username and password:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Try hashed password first
    cur.execute(
        "SELECT * FROM admins WHERE username=%s AND password=%s",
        (username, hashed_password),
    )
    admin = cur.fetchone()

    if not admin:
        # Try plain-text password (legacy)
        cur.execute(
            "SELECT * FROM admins WHERE username=%s AND password=%s",
            (username, password),
        )
        admin = cur.fetchone()
        if admin:
            # Upgrade password to hashed version
            try:
                cur.execute(
                    "UPDATE admins SET password=%s WHERE username=%s",
                    (hashed_password, username),
                )
                con.commit()
            except Exception as e:
                print("Content-type:text/html\r\n\r\n")
                print(f"<h3>Error updating password: {e}</h3>")
                sys.exit(0)

    if admin:
        # Successful login
        cookie = http.cookies.SimpleCookie()
        cookie["admin"] = username
        cookie["admin"]["path"] = "/"
        cookie["admin"]["max-age"] = 3600

        # Send headers for cookie and redirect
        print(cookie.output())
        print("Status: 303 See Other")
        print("Location: admin_page.py\r\n")
        cur.close()
        con.close()
        sys.exit(0)
    else:
        invalid_login()
else:
    # Show login form
    show_login_form()

# Close DB
cur.close()
con.close()
