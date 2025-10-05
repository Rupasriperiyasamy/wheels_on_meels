#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import cgi
import cgitb
import hashlib
import pymysql

cgitb.enable(display=1)  # Show Python errors in browser

print("Content-type: text/html\r\n\r\n")

# Get form data
form = cgi.FieldStorage()
name = form.getvalue("name", "").strip()
email = form.getvalue("email", "").strip()
password = form.getvalue("password", "").strip()
address = form.getvalue("address", "").strip()

# Database connection
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="wheelsonmeals"
)
cur = con.cursor()

# Start HTML
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Registration</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container mt-5">
""")

# Handle form submission
if name and email and password and address:
    hashed = hashlib.sha256(password.encode()).hexdigest()
    try:
        cur.execute(
            "INSERT INTO user_register (full_name, email, password, address) VALUES (%s, %s, %s, %s)",
            (name, email, hashed, address)
        )
        con.commit()
        print(f"""
        <div class="alert alert-success text-center" role="alert">
            <h4 class="alert-heading">Registration Successful!</h4>
            <p>Welcome, {name}! Your account has been created successfully.</p>
            <a href='login_user.py' class="btn btn-primary mt-3">Login Here</a>
        </div>
        """)
    except pymysql.err.IntegrityError:
        print(f"""
        <div class="alert alert-danger text-center" role="alert">
            <h4 class="alert-heading">Email Already Exists!</h4>
            <a href='register_user.py' class="btn btn-warning mt-3">Try Again</a>
        </div>
        """)
else:
    # Registration form
    print("""
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-body">
                    <h2 class="card-title text-center mb-4">User Registration</h2>
                    <form method="post">
                        <div class="mb-3">
                            <label for="name" class="form-label">Full Name:</label>
                            <input type="text" class="form-control" id="name" name="name" required>
                        </div>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email:</label>
                            <input type="email" class="form-control" id="email" name="email" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Password:</label>
                            <input type="password" class="form-control" id="password" name="password" required>
                        </div>
                        <div class="mb-3">
                            <label for="address" class="form-label">Address:</label>
                            <input type="text" class="form-control" id="address" name="address" required>
                        </div>
                        <div class="d-grid">
                            <input type="submit" class="btn btn-primary" value="Register">
                        </div>
                    </form>
                    <p class="text-center mt-3">Already have an account? <a href="login_user.py">Login Here</a></p>
                </div>
            </div>
        </div>
    </div>
    """)

# Close container and HTML
print("""
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")

# Close connection
cur.close()
con.close()
