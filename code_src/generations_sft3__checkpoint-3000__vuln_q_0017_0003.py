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
        self.sessions: Dict[str, Tuple[float, str]] = {}

    def create_session(self) -> str:
        """Create a new session with secure random token"""
        self.session_id = secrets.token_urlsafe(32)
        self.sessions[self.session_id] = (time.time(), self.session_id)
        return self.session_id

    def validate_session(self, session_id: str) -> bool:
        """Validate session exists and hasn't expired"""
        if session_id not in self.sessions:
            return False
        
        session_time, _ = self.sessions[session_id]
        if time.time() - session_time > self.max_age:
            del self.sessions[session_id]
            return False
        
        return True

    def get_session_data(self) -> Dict[str, str]:
        """Get current session data"""
        return {
            "session_id": self.session_id,
            "created_at": html.escape(str(time.time())),
            "csrf_token": secrets.token_urlsafe(32)
        }

class SecureCookieServer:
    def __init__(self, port: int = 8000):
        self.port = port
        self.cookie_handler = SecureCookieHandler()

    def run(self):
        handler = SecureCookieHandlerRequestHandler
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"Serving on port {self.port}")
            httpd.serve_forever()

class SecureCookieHandlerRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse and validate URL
            parsed_path = urllib.parse.urlparse(self.path)
            if parsed_path.path != '/':
                self.send_error(404)
                return

            # Create session if not exists
            session = SecureCookieHandler()
            
            # Prepare response
            response = session.get_session_data()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Set-Cookie', f'session={session.session_id}; HttpOnly; Secure; SameSite=Strict')
            self.end_headers()
            
            self.wfile.write(html.escape(str(response)).encode())

        except Exception as e:
            self.send_error(500, "Internal Server Error")

if __name__ == "__main__":
    server = SecureCookieServer()
    server.run()