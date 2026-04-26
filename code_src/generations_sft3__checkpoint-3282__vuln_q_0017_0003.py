import http.server
import socketserver
import urllib.parse
import secrets
import time
from typing import Dict, Tuple
import html

class SecureCookieHandler:
    def __init__(self, max_age: int = 3600):
        self.session_id = secrets.token_urlsafe(32)
        self.max_age = max_age
        self.cookies: Dict[str, Tuple[str, int]] = {}

    def set_cookie(self, name: str, value: str) -> None:
        """Securely set a cookie with expiration"""
        if not isinstance(name, str) or not isinstance(value, str):
            raise ValueError("Cookie name and value must be strings")
        
        # Sanitize inputs
        name = html.escape(name)
        value = html.escape(value)
        
        # Set secure cookie attributes
        self.cookies[name] = (value, int(time.time()) + self.max_age)

    def get_cookie(self, name: str) -> str:
        """Securely retrieve a cookie value"""
        if not isinstance(name, str):
            raise ValueError("Cookie name must be a string")
        
        name = html.escape(name)
        
        cookie_value, expiration = self.cookies.get(name, ('', 0))
        if expiration > 0 and time.time() > expiration:
            del self.cookies[name]
            return ''
        return cookie_value

    def clear_expired_cookies(self) -> None:
        """Remove expired cookies"""
        current_time = time.time()
        expired = [name for name, (_, exp) in self.cookies.items()
                   if exp <= current_time]
        for name in expired:
            del self.cookies[name]

class SecureRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        """Handle GET requests securely"""
        try:
            # Create secure cookie handler
            cookie_handler = SecureCookieHandler()
            
            # Process query parameters
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)
            
            # Set session cookie
            cookie_handler.set_cookie('session', cookie_handler.session_id)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            
            # Send secure cookies
            for name, value in cookie_handler.cookies.items():
                self.send_header(f'Cookie', f'{name}={value[0]}')
            
            self.end_headers()
            
            # Send HTML response
            response = "<html><body><h1>Welcome</h1></body></html>"
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, "Internal Server Error")
            raise

def run_secure_server(port: int = 8000) -> None:
    """Run a secure HTTP server"""
    with socketserver.TCPServer(("", port), SecureRequestHandler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_secure_server()