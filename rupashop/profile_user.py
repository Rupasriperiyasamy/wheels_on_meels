#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe
import cgi
import cgitb
import pymysql
import os
from http import cookies

cgitb.enable(display=1)

print("Content-type: text/html\r\n\r\n")

# Connect to database
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="wheelsonmeals",
    cursorclass=pymysql.cursors.DictCursor
)
cur = con.cursor()

# Read cookie for logged-in user
cookie = cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
user_cookie = cookie.get("user")

if not user_cookie:
    print("<h3 style='text-align:center; color:red;'>Please <a href='login_user.py'>login</a> first.</h3>")
    exit()

user_email = user_cookie.value.strip()

# Fetch user info
query = "SELECT * FROM user_register WHERE email=%s"
cur.execute(query, (user_email,))
res = cur.fetchone()

if not res:
    print("<h3 style='text-align:center; color:red;'>User not found!</h3>")
    exit()

# Extract user details
name = res.get("full_name", "N/A")
email = res.get("email", "N/A")
address = res.get("address") or "Not provided"
joined = res.get("created_at", "N/A")

# Handle user image safely
image = res.get("user_img")
if not image or image.strip() == "":
    image = "default.png"  # default image in images folder
else:
    image = image.strip()

# HTML Output
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{name} | Profile</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <style>
        body {{ background: #f5f5f5; padding: 20px; }}
        .profile-card {{
            background: #fff; border-radius: 10px; padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            max-width: 700px; margin: auto; text-align:center;
        }}
        .profile-pic {{
            border-radius: 50%; width: 120px; height: 120px;
            object-fit: cover; margin-bottom: 20px;
        }}
        .profile-placeholder {{
            width: 120px; height: 120px; border-radius: 50%;
            background: #007bff; color: #fff;
            display: flex; align-items: center; justify-content: center;
            font-size: 50px; font-weight: bold;
            margin: auto; margin-bottom: 20px;
        }}
        .btn-area {{ margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="profile-card">
""")

# Show image or placeholder
if image == "default.png":
    first_letter = name[0].upper() if name else "U"
    print(f'<div class="profile-placeholder">{first_letter}</div>')
else:
    print(f'<img src="./images/{image}" alt="Profile Picture" class="profile-pic">')

# User details
print(f"""
        <h2>{name}</h2>
        <p><strong>User ID:</strong> {res.get('id', 'N/A')}</p>
        <table class="table table-striped">
            <tr><th>Email</th><td>{email}</td></tr>
            <tr><th>Address</th><td>{address}</td></tr>
            <tr><th>Joined On</th><td>{joined}</td></tr>
        </table>
        <div class="btn-area">
            <a href="home.py" class="btn btn-primary">Go to Home</a>
            <a href="logout_user.py" class="btn btn-danger">Logout</a>
        </div>
    </div>
</body>
</html>
""")

cur.close()
con.close()
