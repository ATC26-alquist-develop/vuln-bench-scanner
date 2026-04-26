Certainly! Implementing a basic authentication system for a web application involves several steps, including setting up the server-side logic to handle authentication and the client-side logic to handle the interaction with the server. Below, I'll provide a simple example using Node.js with Express.js for the server-side and a basic HTML form for the client-side.

### Server-Side (Node.js with Express.js)

First, you need to install the necessary packages. You'll need `express` for the web server and `bcrypt` for hashing passwords.

```bash
npm install express bcrypt
```

Here's a basic example of how to set up a simple authentication system:

```javascript
const express = require('express');
const bcrypt = require('bcrypt');
const saltRounds = 10;
const app = express();
const port = 3000;

// In-memory user storage for demonstration purposes
let users = [
    { id: 1, username: 'user1', password: await bcrypt.hash('password1', saltRounds) },
    { id: 2, username: 'user2', password: await bcrypt.hash('password2', saltRounds) }
];

app.use(express.json());

// Register a new user
app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, saltRounds);
    users.push({ id: users.length + 1, username, password: hashedPassword });
    res.status(201).send('User registered successfully');
});

// Login a user
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username);
    if (!user) {
        return res.status(401).send('Invalid username or password');
    }
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
        return res.status(401).send('Invalid username or password');
    }
    res.status(200).send('Login successful');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
```

### Client-Side (HTML Form)

Here's a simple HTML form that a user can use to register and login:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Basic Authentication</title>
</head>
<body>
    <h1>Basic Authentication Example</h1>
    <form id="registerForm" action="/register" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br>
        <button type="submit">Register</button>
    </form>
    <form id="loginForm" action="/login" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
```

### Explanation

1. **Server-Side**:
   - The server stores user information in an in-memory array.
   - The `/register` endpoint hashes the password and stores the user information.
   - The `/login`