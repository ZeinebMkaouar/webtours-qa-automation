import http.server
import socketserver
import urllib.parse
import threading

PORT = 1080

INDEX_HTML = """<!DOCTYPE html>
<html>
<head><title>Web Tours</title></head>
<frameset rows="65,*" border="1">
    <frame name="header" src="/WebTours/header.html" scrolling="no" />
    <frame name="body" src="/cgi-bin/welcome.pl?signOff=true" />
</frameset>
</html>
"""

HEADER_HTML = """<!DOCTYPE html>
<html><body bgcolor="#003366"><h1 style="color:white;margin:5px;">Web Tours</h1></body></html>
"""

NAV_LOGGED_OUT = """<!DOCTYPE html>
<html>
<body bgcolor="#E0E7F1">
<form method="post" action="/cgi-bin/login.pl" target="body">
    <p>Username: <input type="text" name="username" size="14"/></p>
    <p>Password: <input type="password" name="password" size="14"/></p>
    <p><input type="image" name="login" value="Login" alt="Login" src="/WebTours/images/mer_login.gif"/></p>
</form>
</body>
</html>
"""

NAV_LOGGED_IN = """<!DOCTYPE html>
<html>
<body bgcolor="#E0E7F1">
<center>
    <a href="/cgi-bin/welcome.pl?page=search" target="body"><img src="/WebTours/images/flights.gif" alt="Search Flights Button"/></a><br><br>
    <a href="/cgi-bin/welcome.pl?page=itinerary" target="body"><img src="/WebTours/images/itinerary.gif" alt="Itinerary Button"/></a><br><br>
    <a href="/cgi-bin/welcome.pl?page=menus" target="body"><img src="/WebTours/images/home.gif" alt="Home Button"/></a><br><br>
    <a href="/cgi-bin/welcome.pl?signOff=1" target="body"><img src="/WebTours/images/signoff.gif" alt="SignOff Button"/></a>
</center>
</body>
</html>
"""

INFO_WELCOME = """<!DOCTYPE html>
<html>
<body>
    <h2>Welcome, <b>jojo</b>, to the Web Tours reservation pages.</h2>
    <p>Using the menu to the left, you can search for flights, inspect your itinerary, and sign off.</p>
</body>
</html>
"""

INFO_ERROR = """<!DOCTYPE html>
<html>
<body>
    <h1>Web Tours Error</h1>
    <p>Bad Password. Please re-enter your username and password.</p>
</body>
</html>
"""

INFO_SEARCH = """<!DOCTYPE html>
<html>
<body>
    <h2>Find Flight</h2>
    <form method="post" action="/cgi-bin/reservations.pl" target="info">
        Departure City: 
        <select name="depart">
            <option value="Denver">Denver</option>
            <option value="London">London</option>
            <option value="Paris">Paris</option>
        </select>
        <br><br>
        Arrival City:
        <select name="arrive">
            <option value="London">London</option>
            <option value="Denver">Denver</option>
            <option value="Paris">Paris</option>
        </select>
        <br><br>
        Passengers: <input type="text" name="numPassengers" value="1" />
        <br><br>
        <input type="submit" name="findFlights" value="Continue" />
    </form>
</body>
</html>
"""

INFO_FLIGHTS = """<!DOCTYPE html>
<html>
<body>
    <h2>Select Flight</h2>
    <p>Flight departing from Denver to London</p>
    <form method="post" action="/cgi-bin/reservations.pl" target="info">
        <input type="radio" name="outboundFlight" value="001" checked /> Flight 001 - 08:00 AM - $250<br><br>
        <input type="submit" name="reserveFlights" value="Continue" />
    </form>
</body>
</html>
"""

INFO_PAYMENT = """<!DOCTYPE html>
<html>
<body>
    <h2>Payment Details</h2>
    <form method="post" action="/cgi-bin/reservations.pl" target="info">
        Credit Card: <input type="text" name="creditCard" /><br><br>
        Exp Date: <input type="text" name="expDate" /><br><br>
        <input type="submit" name="buyFlights" value="Continue" />
    </form>
</body>
</html>
"""

INFO_INVOICE = """<!DOCTYPE html>
<html>
<body>
    <h1>Invoice</h1>
    <h2>Reservation Made!</h2>
    <p>Thank you for booking through Web Tours.</p>
    <p>Flight departing from Denver to London confirmed.</p>
</body>
</html>
"""

def make_frameset(nav_src, info_src):
    return f"""<!DOCTYPE html>
<html>
<frameset cols="160,*" border="1">
    <frame name="navbar" src="{nav_src}" />
    <frame name="info" src="{info_src}" />
</frameset>
</html>
"""

class MockWebToursHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Silence logging

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        if path == "/" or path == "/WebTours/index.htm":
            self.wfile.write(INDEX_HTML.encode("utf-8"))
        elif path == "/WebTours/header.html":
            self.wfile.write(HEADER_HTML.encode("utf-8"))
        elif path == "/cgi-bin/welcome.pl":
            if query.get("signOff") or query.get("page") == ["logout"]:
                self.wfile.write(make_frameset("/cgi-bin/nav.pl?in=home", "/WebTours/home.html").encode("utf-8"))
            elif query.get("page") == ["search"]:
                self.wfile.write(make_frameset("/cgi-bin/nav.pl?page=menu", "/cgi-bin/search.html").encode("utf-8"))
            else:
                self.wfile.write(make_frameset("/cgi-bin/nav.pl?page=menu", "/cgi-bin/info_welcome.html").encode("utf-8"))
        elif path == "/cgi-bin/nav.pl":
            if query.get("page") == ["menu"]:
                self.wfile.write(NAV_LOGGED_IN.encode("utf-8"))
            else:
                self.wfile.write(NAV_LOGGED_OUT.encode("utf-8"))
        elif path == "/WebTours/home.html":
            self.wfile.write(b"<html><body><h1>Welcome to the Web Tours site</h1></body></html>")
        elif path == "/cgi-bin/info_welcome.html":
            self.wfile.write(INFO_WELCOME.encode("utf-8"))
        elif path == "/cgi-bin/info_error.html":
            self.wfile.write(INFO_ERROR.encode("utf-8"))
        elif path == "/cgi-bin/search.html":
            self.wfile.write(INFO_SEARCH.encode("utf-8"))
        else:
            self.wfile.write(b"<html><body>OK</body></html>")

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len).decode("utf-8", errors="ignore")
        params = urllib.parse.parse_qs(body)

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        if path == "/cgi-bin/login.pl":
            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]
            if username == "jojo" and password == "bean":
                self.wfile.write(make_frameset("/cgi-bin/nav.pl?page=menu", "/cgi-bin/info_welcome.html").encode("utf-8"))
            else:
                self.wfile.write(make_frameset("/cgi-bin/nav.pl?in=home", "/cgi-bin/info_error.html").encode("utf-8"))
        elif path == "/cgi-bin/reservations.pl":
            if "findFlights" in params or "findFlights.x" in params:
                self.wfile.write(INFO_FLIGHTS.encode("utf-8"))
            elif "reserveFlights" in params or "reserveFlights.x" in params:
                self.wfile.write(INFO_PAYMENT.encode("utf-8"))
            elif "buyFlights" in params or "buyFlights.x" in params:
                self.wfile.write(INFO_INVOICE.encode("utf-8"))
            else:
                self.wfile.write(INFO_SEARCH.encode("utf-8"))
        else:
            self.wfile.write(b"<html><body>OK</body></html>")

def start_server_in_thread():
    server = socketserver.TCPServer(("127.0.0.1", PORT), MockWebToursHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server

if __name__ == "__main__":
    print(f"Starting mock Web Tours on port {PORT}...")
    server = socketserver.TCPServer(("127.0.0.1", PORT), MockWebToursHandler)
    server.serve_forever()
