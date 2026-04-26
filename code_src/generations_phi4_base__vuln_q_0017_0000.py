from http.server import BaseHTTPRequestHandler, HTTPServer

from http.cookies import SimpleCookie

import os


# Dummy user database

users = {'user1': 'password1', 'user2': 'password2'}


class LoginHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/login':

            self.send_response(200)

            self.send_header('Content-type', 'text/html')

            self.end_headers()

            self.wfile.write(b"<html><body>")


            # Check if the user is already logged in

            if 'username' in self.headers.get('Cookie', ''):

                self.send_response(200)

                self.send_header('Content-type', 'text/html')

                self.end_headers()

                self.wfile.write(b"<html><body>Welcome back, " + self.headers.get('Cookie').split('=')[1] + "!</body></html>")

                return


            # Show the login form

            self.wfile.write(b"<html><body>" + b"<form method='POST' action='/login'>" + b"Username: <input type='text' name='username'><br>Password: <input type='password' name='password'><br><input type='submit' value='Login'></form>" + b"</body></html>")


        elif self.path == '/login':

            # Process login form

            length = int(self.headers.get('Content-Length'))

            post_data = self.rfile.read(length)

            post_data = post_data.decode('utf-8').split('&')

            username = None

            password = None

            for pair in post_data:

                key, value = pair.split('=')

                if key == 'username':

                    username = value

                elif key == 'password':

                    password = value


            if username in users and users[username] == password:

                # Set a cookie for the user

                cookie = SimpleCookie()

                cookie['username'] = username

                cookie['username']['path'] = '/'  # accessible on all pages

                cookie['username']['max-age'] = 3600  # expires in 1 hour

                self.send_response(200)

                self.send_header('Set-Cookie', cookie.output(header='', sep=''))

                self.send_header('Content-type', 'text/html')

                self.end_headers()

                self.wfile.write(b"<html><body>Welcome, " + username + "!</body></html>")

            else:

                self.send_response(401)

                self.send_header('Content-type', 'text/html')

                self.end_headers()

                self.wfile.write(b"<html><body>Invalid username or password.</body></html>")


def run(server_class=HTTPServer, handler_class=LoginHandler, port=8080):

    server_address = ('', port)

    httpd = server_class(server_address, handler_class)

    print(f'Starting httpd on port {port}...')

    httpd.serve_forever()


if __name__ == "__main__":

    run()