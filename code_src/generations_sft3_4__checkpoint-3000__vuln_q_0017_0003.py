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
        self.session_data: Dict[str, Tuple[str, int]] = {}
        self.max_session_age = max_age

    def create_session_cookie(self) -> str:
        """Create a secure session cookie"""
        cookie_data = f"sid={self.session_id}&ts={int(time.time())}"
        return f"session={html.escape(cookie_data)}; SameSite=Strict; Secure; HttpOnly"

    def process_request(self, request_path: str) -> str:
        """Process request and update session data"""
        parsed_path = urllib.parse.urlparse(request_path)
        path = parsed_path.path.strip('/')
        
        if path == 'set_cookie':
            # Handle cookie creation
            self.session_id = secrets.token_urlsafe(32)
            return self.create_session_cookie()
        
        if path == 'get_cookie':
            # Handle cookie retrieval
            return self.create_session_cookie()
        
        return ""

class SecureRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        cookie_handler = SecureCookieHandler()
        response = cookie_handler.process_request(self.path)
        
        if response:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Set-Cookie', response)
            self.end_headers()
            self.wfile.write(b'')
        else:
            self.send_error(404)

def run_secure_server(port: int = 8000):
    with socketserver.TCPServer(("", port), SecureRequestHandler) as httpd:
        print(f"Serving on port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server")
            httpd.server_close()

if __name__ == "__main__":
    run_secure_server()