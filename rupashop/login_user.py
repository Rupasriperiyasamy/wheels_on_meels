#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe
import cgi
import cgitb
import hashlib
import pymysql
import http.cookies
import sys
sys.stdout.reconfigure(encoding='utf-8')

cgitb.enable(display=1)

form = cgi.FieldStorage()
email = form.getvalue("email", "").strip()
password = form.getvalue("password", "").strip()

con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="wheelsonmeals",
    cursorclass=pymysql.cursors.DictCursor
)
cur = con.cursor()

if email and password:
    hashed = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT * FROM user_register WHERE email=%s AND password=%s", (email, hashed))
    user = cur.fetchone()

    if user:
        # Set cookie
        cookie = http.cookies.SimpleCookie()
        cookie["user"] = email
        cookie["user"]["path"] = "/"
        cookie["user"]["max-age"] = 3600  # 1 hour

        # Headers first
        print("Content-type: text/html")
        print(cookie.output())
        print("\r\n")

        # Success HTML
        print(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Login Success</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </head>
        <body class="bg-light">

        <div class="container mt-5 text-center">
            <h2>Welcome, {user['full_name']}!</h2>
            <p>Login Successful ✅</p>
            <a href="profile_user.py" class="btn btn-info">View Profile</a>
            <a href="home.py" class="btn btn-primary">Go to Home</a>
        </div>

        </body>
        </html>
        """)
    else:
        print("Content-type: text/html\r\n\r\n")
        print("""
        <!DOCTYPE html>
        <html lang="en">
        <head><meta charset="UTF-8"><title>Login Failed</title></head>
        <body>
        <h2 style="color:red; text-align:center;">Invalid Credentials!</h2>
        <a href='login_user.py'>Try Again</a>
        </body>
        </html>
        """)

else:
    print("Content-type: text/html\r\n\r\n")
    print("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>User Login</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6 bg-white p-4 rounded shadow">
                <h2 class="text-center mb-4">User Login</h2>
                <form method="post">
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" name="email" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                    <p class="mt-3 text-center">Don't have an account? <a href="register_user.py">Register here</a></p>
                </form>
            </div>
        </div>
    </div>
    </body>
    </html>
    """)

cur.close()
con.close()
