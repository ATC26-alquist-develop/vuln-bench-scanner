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
        cookies = dict(item.split('=') for item in cookie_value.split(';') if item.strip())
        
        if self.cookie_name in cookies:
            # Parse timestamp if cookie exists
            try:
                timestamp, visit_count = cookies[self.cookie_name].split(',')
                timestamp = int(timestamp)
                visit_count = int(visit_count)
            except (ValueError, KeyError):
                return ''
        else:
            # Generate new cookie
            timestamp = int(time.time())
            visit_count = 1
            
        # Check cookie expiration
        if time.time() - timestamp > self.max_age:
            visit_count = 1
            timestamp = int(time.time())
        
        # Update visit count
        self.visits[self.cookie_name] = (timestamp, visit_count)
        
        # Create secure cookie string
        cookie = f"{self.cookie_name}={visit_count}; SameSite=Strict"
        return cookie

    def get_visits(self) -> Dict[str, int]:
        """Get current visit counts."""
        return {cookie: count for cookie, (_, count) in self.visits.items()}

class SecureTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def run_secure_server(port: int = 8000):
    """Run a simple secure server."""
    handler = SecureCookieHandler()
    
    try:
        with SecureTCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"Serving on port {port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Server error: {e}")
        return

if __name__ == "__main__":
    run_secure_server()