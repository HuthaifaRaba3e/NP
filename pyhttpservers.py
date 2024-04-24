from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import base64

# Define user credentials (for demo purposes)
USER = "admin"
PASSWORD = "password"

# HTTP Request Handler
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check for authentication
        if not self.authenticate():
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="PyHTTPServer"')
            self.end_headers()
            self.wfile.write(b"Authentication required")
            return

        # Serve static or dynamic content based on the request path
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Welcome to PyHTTPServer!</h1>")
        elif self.path == "/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {"message": "This is dynamic content"}
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif self.path == "/image":
            # Serve the specific image file
            image_path = os.path.join("static", "lovepik-natural-woods-png-image_401110806_wh1200.png")
            if os.path.exists(image_path) and os.path.isfile(image_path):
                self.send_response(200)
                self.send_header("Content-type", "image/png")  # Set the content type for PNG image
                self.end_headers()
                with open(image_path, "rb") as image_file:
                    self.wfile.write(image_file.read())
        else:
            # Try to serve static files from the 'static' directory
            static_file_path = os.path.join("static", self.path.lstrip("/"))
            if os.path.exists(static_file_path) and os.path.isfile(static_file_path):
                self.send_response(200)
                self.send_header("Content-type", self.guess_content_type(static_file_path))
                self.end_headers()
                with open(static_file_path, "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"404 Not Found")


    def authenticate(self):
        auth_header = self.headers.get("Authorization")
        if auth_header:
            auth_type, auth_token = auth_header.split()
            if auth_type.lower() == "basic":
                decoded_token = base64.b64decode(auth_token).decode("utf-8")
                username, password = decoded_token.split(":")
                return username == USER and password == PASSWORD
        return False

    def guess_content_type(self, file_path):
        """Guess the content type based on the file extension."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == ".html":
            return "text/html"
        elif ext == ".css":
            return "text/css"
        elif ext == ".js":
            return "application/javascript"
        elif ext == ".png":
            return "image/png"
        elif ext == ".jpg" or ext == ".jpeg":
            return "image/jpeg"
        else:
            return "application/octet-stream"  # default to binary data

# Main function to start the server
def run_server():
    server_address = ("", 8035)  # Use localhost and port 8000
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print("Starting PyHTTPServer...")
    httpd.serve_forever()

# Run the server
if __name__ == "__main__":
    run_server()
