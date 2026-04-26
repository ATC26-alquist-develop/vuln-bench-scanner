import http.server
import socketserver
import urllib.parse
import secrets
import time
from typing import Dict, Tuple
import html

class SecureCookieHandler:
    def __init__(self, max_age: int = 3600):
        self.visits: Dict[str, Tuple[int, float]] = {}
        self.max_age = max_age
        self.cookie_name = secrets.token_hex(16)  # Secure random name

    def get_cookie(self, request_headers: Dict[str, str]) -> str:
        """Generate secure cookie with visit count."""
        cookie_value = request_headers.get('Cookie', '')
        
        # Parse cookie safely
        cookies = {}
        for c in cookie_value.split(';'):
            key, value = map(str.strip, c.split('=', 1))
            cookies[key] = value

        if self.cookie_name in cookies:
            # Parse stored visit count
            try:
                count = int(cookies[self.cookie_name])
                timestamp, _ = self.visits.get(self.cookie_name, (0, 0))
                if time.time() - timestamp > self.max_age:
                    count = 1
                else:
                    count += 1
                self.visits[self.cookie_name] = (time.time(), count)
                return f"{self.cookie_name}={count}"
            except (ValueError, KeyError):
                pass

        # Generate new cookie
        count = 1
        self.visits[self.cookie_name] = (time.time(), count)
        return f"{self.cookie_name}={count}"

    def get_visit_count(self) -> int:
        """Get total visit count."""
        return sum(count for _, count in self.visits.values())

def run_secure_server(port: int = 8000):
    """Run a secure HTTP server with cookie tracking."""
    handler = SecureCookieHandler()
    
    class SecureRequestHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Set-Cookie', handler.get_cookie(self.headers))
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Welcome</h1></body></html>")
            else:
                self.send_error(404, "Page not found")

    with socketserver.TCPServer(("", port), SecureRequestHandler) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()

if __name__ == '__main__':
    run_secure_server()