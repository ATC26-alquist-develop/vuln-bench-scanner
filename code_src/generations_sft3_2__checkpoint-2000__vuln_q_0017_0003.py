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
        self._cookie_store: Dict[str, Tuple[float, str]] = {}
        self._cookie_expiry = 3600  # 1 hour

    def do_GET(self) -> None:
        """Handle GET requests with secure cookie handling."""
        # Parse URL safely
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Check for secure cookie
        cookie = self.get_secure_cookie()
        
        if cookie:
            # Update cookie expiration
            self._cookie_store[cookie] = (time.time(), cookie)
            
            # Prepare response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Render page with secure cookie info
            self.wfile.write(self.render_page(cookie))
        else:
            # Handle no cookie case
            self.send_error(403, "No secure cookie found")

    def get_secure_cookie(self) -> str:
        """Securely retrieve and validate cookie."""
        cookie = self.headers.get('Cookie')
        if not cookie:
            return ''
            
        # Parse cookie safely
        cookies = dict(item.split('=') for item in cookie.split(';'))
        
        # Validate cookie format
        if 'securecookie=' not in cookies:
            return ''
            
        return cookies['securecookie']

    def render_page(self, cookie: str) -> bytes:
        """Render page with secure cookie information."""
        # Sanitize cookie value
        safe_cookie = html.escape(cookie)
        
        # Generate secure response
        response = f"""
        <html>
        <head>
            <title>Secure Cookie Example</title>
        </head>
        <body>
            <h1>Welcome to Secure Cookie Example</h1>
            <p>Your secure cookie: {safe_cookie}</p>
            <p>Cookie last updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self._cookie_store[cookie][0]))}</p>
        </body>
        </html>
        """
        return response.encode('utf-8')

def run_secure_server(port: int = 8000) -> None:
    """Run a secure HTTP server."""
    handler = SecureCookieHandler
    handler.server_version = 'SecureCookieHandler/1.0'
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving on port {port}")
        httpd.serve_forever()

if __name__ == '__main__':
    run_secure_server()