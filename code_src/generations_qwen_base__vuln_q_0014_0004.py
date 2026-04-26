from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulate a user database
users = {'user1': 'password1'}

@app.before_request
def check_user():
    if request.endpoint not in ['login', 'home', 'logout'] and 'username' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials'
    return '''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/home')
def home():
    return 'Welcome to the home page!'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

# ===== cell separator =====

# settings.py
MIDDLEWARE = [
    # Other middleware
    'yourapp.middleware.LoginRequiredMiddleware',
]

# yourapp/middleware.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        redirect_url = reverse('login')
        if request.path not in [reverse('login'), reverse('logout')] and not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

# yourapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def logout(request):
    return redirect('login')