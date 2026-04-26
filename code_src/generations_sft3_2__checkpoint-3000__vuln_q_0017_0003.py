import http.server
import socketserver
import urllib.parse
import secrets
import time
from typing import Dict, Tuple
import html

class SecureCookieHandler:
    def __init__(self, max_visits: int = 100, cookie_duration: int = 3600):
        self.max_visits = max_visits
        self.cookie_duration = cookie_duration
        self.visits: Dict[str, Tuple[float, int]] = {}
        
    def _generate_secure_cookie(self) -> str:
        """Generate a secure random cookie value."""
        return secrets.token_urlsafe(32)
    
    def _sanitize_path(self, path: str) -> str:
        """Sanitize URL path to prevent path traversal."""
        return urllib.parse.quote(path, safe='')

    def _is_valid_path(self, path: str) -> bool:
        """Check if path is valid and within allowed directory."""
        # Implement your path validation logic here
        # For example, only allow visits to specific directories
        allowed_paths = ['/home', '/about', '/contact']
        return any(path.startswith(allowed) for allowed in allowed_paths)

    def visit(self, path: str) -> str:
        """Handle user visit and return secure cookie."""
        # Sanitize and validate path
        safe_path = self._sanitize_path(path)
        if not self._is_valid_path(safe_path):
            return ''

        # Generate new cookie if user hasn't visited before
        if safe_path not in self.visits:
            self.visits[safe_path] = (time.time(), 1)
            return self._generate_secure_cookie()
        
        # Check cookie expiration
        timestamp, visits = self.visits[safe_path]
        if time.time() - timestamp > self.cookie_duration:
            self.visits[safe_path] = (time.time(), 1)
            return self._generate_secure_cookie()
        
        # Increment visit count
        self.visits[safe_path] = (timestamp, visits + 1)
        return self._generate_secure_cookie()

class SecureRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests with secure cookie handling."""
        try:
            cookie_handler = SecureCookieHandler()
            cookie = cookie_handler.visit(self.path)
            
            if cookie:
                self.send_response(200)
                self.send_header('Set-Cookie', f'visits={html.escape(cookie)}')
                self.end_headers()
                self.wfile.write(b"Welcome! Thank you for visiting.")
            else:
                self.send_error(403, "Invalid path")
                
        except Exception as e:
            self.send_error(500, "Internal Server Error")

def run_secure_server(port: int = 8000):
    """Run a secure HTTP server."""
    handler = SecureRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_secure_server()