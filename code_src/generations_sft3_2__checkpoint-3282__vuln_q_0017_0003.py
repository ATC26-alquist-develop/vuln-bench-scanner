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
    
    def _sanitize_input(self, input_str: str) -> str:
        """Sanitize input to prevent injection attacks."""
        return html.escape(input_str)
    
    def track_visit(self, request: http.server.SimpleHTTPRequest) -> None:
        """Track a user visit securely."""
        try:
            # Get and validate cookie
            cookie = request.headers.get('Cookie')
            if not cookie:
                return
                
            # Parse cookie safely
            cookies = dict(urllib.parse.parse_qsl(cookie))
            
            # Generate unique visit ID
            visit_id = secrets.token_urlsafe(16)
            
            # Check if visit exists
            if visit_id in self.visits:
                timestamp, count = self.visits[visit_id]
                # Check if cookie has expired
                if time.time() - timestamp > self.cookie_duration:
                    self.visits[visit_id] = (time.time(), 1)
                else:
                    self.visits[visit_id] = (timestamp, count + 1)
            else:
                self.visits[visit_id] = (time.time(), 1)
            
            # Set secure cookie
            secure_cookie = f"visits={visit_id}; SameSite=Strict; Secure; HttpOnly"
            request.responseHeaders['Set-Cookie'] = secure_cookie
            
        except Exception:
            # Fail securely
            pass

class SecureHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests securely."""
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                # Track visit
                handler = SecureCookieHandler()
                handler.track_visit(self)
                
                # Generate safe response
                response = "<html><body><h1>Welcome to Secure Website</h1></body></html>"
                self.wfile.write(response.encode('utf-8'))
            else:
                self.send_error(404, "Page not found")
                
        except Exception:
            self.send_error(500, "Internal Server Error")

if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(("", PORT), SecureHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()