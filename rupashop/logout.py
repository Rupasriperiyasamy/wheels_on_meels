#!C:/Users/Sakthivelpalani/AppData/Local/Programs/Python/Python311/python.exe

import http.cookies

# Expire the cookie
cookie = http.cookies.SimpleCookie()
cookie["user"] = ""
cookie["user"]["path"] = "/"
cookie["user"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"

# Print headers
print("Content-type: text/html")
print(cookie.output())
print("Refresh: 5; url=/rupashop/login_user.py")
print()  # end headers

# HTML output
print("""
<html>
  <body style="font-family: Arial; text-align:center; margin-top:50px;">
    <h2>You have been logged out successfully.</h2>
    <p>Redirecting to login page...</p>
    <p>If not redirected, <a href="/cgi-bin/home.py">click here</a>.</p>
  </body>
</html>
""")
