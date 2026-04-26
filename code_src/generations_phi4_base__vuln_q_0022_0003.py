Creating an admin dashboard for a user management system involves several steps, including designing the user interface, setting up the backend to handle user data, and integrating both components. Below is a high-level overview of how you can create an admin dashboard for a user management system using a combination of HTML, CSS, JavaScript, and a backend technology like Node.js with Express.

### Step 1: Set Up the Project Structure
Create a new project directory and initialize it with npm:

```bash
mkdir user-management-dashboard
cd user-management-dashboard
npm init -y
```

Install necessary packages:

```bash
npm install express ejs body-parser
```

Create the following directory structure:

```
/user-management-dashboard
  /public
    /css
      style.css
    /js
      dashboard.js
  /views
    index.ejs
  app.js
```

### Step 2: Set Up the Backend (app.js)
Create an Express server and set up routes to handle user data.

```javascript
// app.js
const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));

// Dummy user data
let users = [
  { id: 1, name: 'John Doe', email: 'john@example.com' },
  { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
];

// Routes
app.get('/', (req, res) => {
  res.render('index', { users });
});

app.post('/add-user', (req, res) => {
  const { name, email } = req.body;
  const newUser = { id: users.length + 1, name, email };
  users.push(newUser);
  res.redirect('/');
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
```

### Step 3: Create the Frontend (views/index.ejs)
Create an EJS template for the admin dashboard.

```html
<!-- views/index.ejs -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>User Management Dashboard</title>
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <h1>User Management Dashboard</h1>
  <form action="/add-user" method="POST">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name" required>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required>
    <button type="submit">Add User</button>
  </form>
  <ul>
    <% users.forEach(user => { %>
      <li><%= user.name %> - <%= user.email %></li>
    <% }) %>
  </ul>
  <script src="/js/dashboard.js"></script>
</body>
</html>
```

### Step 4: Add Styling (public/css/style.css)
Add some basic styles to your dashboard.

```css
/* public/css/style.css */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
}

h1 {
  text-align: center;
  margin-top: 20px;
}

form {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ccc;