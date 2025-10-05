#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import sys
import cgitb
import pymysql
import http.cookies
import os

cgitb.enable()
sys.stdout.reconfigure(encoding='utf-8')  # Ensure UTF-8 output

print("Content-type:text/html\r\n\r\n")

# Check user login
cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
user_email = cookie["user"].value if "user" in cookie else None

# Connect to database
con = pymysql.connect(host="localhost", user="root", password="", database="wheelsonmeals")
cur = con.cursor()

# Fetch all products
cur.execute("SELECT id, name, description, price, image FROM products")
products = cur.fetchall()

# HTML output
print("""
<html>
<head>
    <title>Wheels on Meals</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {
            background-color: #f8f9fa;
        }
        .video-container {
            position: relative;
            width: 100%;
            height: 90vh;
            overflow: hidden;
        }
        .video-container video {
            position: absolute;
            top: 50%;
            left: 50%;
            min-width: 100%;
            min-height: 100%;
            transform: translate(-50%, -50%);
            object-fit: cover;
        }
        .video-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #fff;
            text-align: center;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.7);
        }
        .video-overlay h1 {
            font-size: 3rem;
            font-weight: bold;
        }
        .video-overlay p {
            font-size: 1.2rem;
        }
        footer {
            background-color: #343a40;
            color: #fff;
            padding: 40px 0;
        }
        footer a {
            color: #ffc107;
            text-decoration: none;
        }
        footer a:hover {
            text-decoration: underline;
        }
        .footer-logo {
            max-height: 60px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

<!-- Navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-danger sticky-top">
  <div class="container">
    <a class="navbar-brand" href="#"><img src="./asset/logo.png" height="60" width="150"></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="index.py"><i class="fas fa-home"></i> Home</a></li>
        <li class="nav-item"><a class="nav-link" href="cart.py"><i class="fas fa-shopping-cart"></i> Cart</a></li>
        <li class="nav-item"><a class="nav-link" href="login_user.py"><i class="fas fa-user"></i> Login</a></li>
        <li class="nav-item">
        <a class="btn btn-outline-light ms-2" href="register_user.py"><i class="fas fa-user-plus"></i> Register</a>
    </li>
      </ul>
      
    </div>
  </div>
</nav>

<!-- Video Section -->
<div class="video-container">
    <video autoplay loop muted playsinline>
        <source src="./asset/FOOD.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <div class="video-overlay">
        <h1>Welcome to Wheels on Meals</h1>
        <p>Delicious food delivered to your doorstep</p>
    </div>
</div>
<div class="icon mt-5 text-center">
  <marquee direction="right">
    <span class="text-danger">
      <i class="fa fa-truck fa-3x" aria-hidden="true"><b> ......PLACE ORDER.......</b></i>
    </span>
  </marquee>
</div>
<!--ITEMS-->
<div class="container my-5">
  <h2 class="text-center mb-4">Popular Dishes</h2>

  <div class="d-flex overflow-auto pb-3">
    <img src="./asset/1.png" alt="Dish 1" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;  ">
    <img src="./asset/2.png" alt="Dish 2" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/3.png" alt="Dish 3" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/4.png" alt="Dish 4" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/5.png" alt="Dish 5" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/13.png" alt="Dish 6" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/7.png" alt="Dish 7" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/8.png" alt="Dish 8" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/9.png" alt="Dish 9" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/0.png" alt="Dish 10" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/11.png" alt="Dish 11" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
    <img src="./asset/12.png" alt="Dish 12" class="mr-3" style="flex: 0 0 auto; border-radius: 8px; max-height: 200px;">
  </div>
</div>

<div class="container my-5">
    <h2 class="text-center mb-4">Our Products</h2>
    <div class="row row-cols-1 row-cols-md-3 g-4">
""")
for pid, name, desc, price, img in products:
    img_path = img if img and img.startswith("uploads/") else f"uploads/{img}"  # fallback
    if user_email:
        add_cart_button = f'<a class="btn btn-primary me-2" href="add_to_cart.py?product_id={pid}&product_name={name}&price={price}">Add to Cart</a>'
    else:
        add_cart_button = '<small>Please <a href="login_user.py">login</a> to add to cart</small>'

    print(f"""
        <div class="col">
            <div class="card h-100 shadow-sm">
                <img src="{img_path}" class="card-img-top" alt="{name}" style="height:200px; object-fit:cover;">
                <div class="card-body text-center">
                    <h5 class="card-title">{name}</h5>
                    <p class="card-text">{desc}</p>
                    <p class="fw-bold text-danger">&#8377;{price}</p>
                    {add_cart_button}
                </div>
            </div>
        </div>
    """)

print("""
    </div>
</div>

<!-- Footer -->
<footer class="mt-5 bg-danger text-white">
    <div class="container">
        <div class="row text-center text-md-start">
            <div class="col-md-4 mb-3">
                <img src="./asset/logo.png" class="footer-logo img-fluid" alt="Wheels on Meals">
                <p>Wheels on Meals</p>
            </div>
            <div class="col-md-4 mb-3">
                <h5>Contact Us</h5>
                <p>Email: support@wheelsonmeals.com</p>
                <p>Phone: +91 9876543210</p>
                <p>Address: 123 Food Street, City</p>
            </div>
            <div class="col-md-4 mb-3">
                <h5>Follow Us</h5>
                <a href="#" class="text-white"><i class="fab fa-facebook fa-lg me-2"></i></a>
                <a href="#" class="text-white"><i class="fab fa-twitter fa-lg me-2"></i></a>
                <a href="#" class="text-white"><i class="fab fa-instagram fa-lg"></i></a>
            </div>
            <hr>
         <div bg-color=danger class="text-center py-3">
    &copy; 2025 Wheels on Meals. All rights reserved.
  </div>
</footer>


<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
""")
