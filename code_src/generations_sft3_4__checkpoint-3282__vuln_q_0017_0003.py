import http.server
import socketserver
import secrets
import time
from urllib.parse import urlparse, parse_qs
import html

class SecureCookieHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests with secure cookie management"""
        try:
            # Generate secure random cookie ID
            cookie_id = secrets.token_urlsafe(32)
            
            # Create secure cookie with HTTP-only flag
            cookie = http.cookies.SimpleCookie()
            cookie['user_visit'] = cookie_id
            cookie['user_visit']['httponly'] = True
            cookie['user_visit']['max-age'] = 3600  # 1 hour
            
            # Parse and validate query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Validate and sanitize user input
            if 'username' in query_params:
                username = html.escape(query_params['username'][0])
                if len(username) <= 50:  # Reasonable length limit
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Set-Cookie', cookie.output().decode())
                    self.end_headers()
                    
                    # Log visit securely
                    self.log_message(f"User {username} visited at {time.time()}")
                    
                    self.wfile.write(b"Welcome! Your visit is tracked securely.")
                else:
                    self.send_error(400, "Invalid username length")
            else:
                self.send_error(400, "Missing username parameter")

        except Exception as e:
            self.log_error(f"Error handling request: {str(e)}")
            self.send_error(500, "Internal Server Error")

if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(("", PORT), SecureCookieHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()