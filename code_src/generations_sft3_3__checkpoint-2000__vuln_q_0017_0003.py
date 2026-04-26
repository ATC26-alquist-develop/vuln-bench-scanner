import http.server
import socketserver
import urllib.parse
import secrets
import time
from typing import Dict, Tuple
import html

class SecureCookieHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cookie_store: Dict[str, Tuple[str, float]] = {}
        self._cookie_expiry = 3600  # 1 hour

    def do_GET(self) -> None:
        """Handle GET requests with secure cookie handling."""
        # Parse and validate the path
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path != '/':
            self.send_error(403, "Forbidden")
            return

        # Generate secure random cookie ID
        cookie_id = secrets.token_urlsafe(32)
        
        # Create secure cookie
        cookie = http.cookies.SimpleCookie()
        cookie['user_visit'] = cookie_id
        cookie['user_visit']['httponly'] = True
        cookie['user_visit']['secure'] = True
        cookie['user_visit']['samesite'] = 'Strict'
        cookie['user_visit']['max-age'] = self._cookie_expiry
        cookie['user_visit']['path'] = '/'
        
        # Store visit information
        self._cookie_store[cookie_id] = (time.time(), self.client_address[0])
        
        # Send response with cookie
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Set-Cookie', cookie.output())
        self.end_headers()
        
        # Send HTML response
        self.wfile.write(b"<html><body><h1>Welcome</h1></body></html>")

    def log_message(self, format: str, *args: object) -> None:
        """Override to disable logging"""
        pass

def run_server(port: int = 8000) -> None:
    """Run the secure server."""
    handler = SecureCookieHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()