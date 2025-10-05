#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import http.cookies
import os

cookie = http.cookies.SimpleCookie()
cookie["admin"] = ""
cookie["admin"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
cookie["admin"]["path"] = "/"

# Redirect to login page with a query parameter
print(cookie.output())
print("Location: admin_login.py?msg=logout_success")
print()
