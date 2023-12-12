// Function to handle login form submit
function loginFormSubmit(event) {
  event.preventDefault();

  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: email,
      password
    })
  }).then(response => response.json())
    .then(data => {
      if (data.message === 'Login successful') {
        // Store access token in local storage
        localStorage.setItem('access_token', data.access_token);
        window.location.href = '/dashboard';
      } else {
        alert(data.error);
      }
    })
    .catch(error => {
      console.error(error);
      alert('Internal server error. Please try again later.');
    });
}

// Function to handle register form submit
function registerFormSubmit(event) {
  event.preventDefault();

  const name = document.getElementById('register-name').value;
  const email = document.getElementById('register-email').value;
  const password = document.getElementById('register-password').value;

  fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: name,
      email,
      password
    })
  }).then(response => response.json())
    .then(data => {
      if (data.user_id) {
        alert('Registration successful. Please login to continue.');
      } else {
        alert(data.error);
      }
    })
    .catch(error => {
      console.error(error);
      alert('Internal server error. Please try again later.');
    });
}

const loginForm = document.querySelector('.login-form');
loginForm.addEventListener('submit', function (event) {
  event.preventDefault();

  const username = document.querySelector('#username').value;
  const password = document.querySelector('#password').value;

  // Validate username and password
  if (!username || !password) {
    // Display error message
    flash('Please enter both username and password.', 'danger');
    return;
  }

  // Send POST request to login endpoint
  fetch('/login', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Login successful
        // ...
      } else {
        // Display error message
        flash(data.error, 'danger');
      }
    });

  if (data.success) {
    // Store access token (if used)
    localStorage.setItem('accessToken', data.accessToken);
    // Redirect to desired page
    window.location.href = url_for('dashboard');
  }

  if (!data.success) {
    // Display error message
    flash(data.error, 'danger');
  }
});

const registerForm = document.querySelector('.register-form');
registerForm.addEventListener('submit', function (event) {
  event.preventDefault();

  const username = document.querySelector('#username').value;
  const email = document.querySelector('#email').value;
  const password = document.querySelector('#password').value;

  // Validate username, email, and password
  if (!username || !email || !password) {
    // Display error message
    flash('Please fill in all required fields.', 'danger');
    return;
  }

  // Send POST request to register endpoint
  fetch('/register', {
    method: 'POST',
    body: JSON.stringify({ username, email, password })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        // Registration successful
        // ...
      } else {
        // Display error message
        flash(data.error, 'danger');
      }
    });

  if (data.success) {
    // Redirect to login page
    window.location.href = url_for('login');
  }

  if (!data.success) {
    // Display error message
    flash(data.error, 'danger');
  }
});

// Check for access token in local storage
const accessToken = localStorage.getItem('access_token');

if (accessToken) {
  fetch('/dashboard', {
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  }).then(response => response.json())
    .then(data => {
      if (data.message) {
        // User is logged in, render dashboard content
        // ...
      } else {
        // Invalid access token, redirect to login page
        window.location.href = '/login';
      }
    })
    .catch(error => {
      console.error(error);
      alert('Internal server error. Please try again later.');
    });
} else {
  window.location.href = '/login';
}

// Function to handle logout
function logout() {
  fetch('/logout', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  }).then(response => response.json())
    .then(data => {
      if (data.message === 'Logout successful') {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      } else {
        alert(data.error);
      }
    })
    .catch(error => {
      console.error(error);
      alert('Internal server error. Please try again later.');
    });
}

// Add click event listener to logout button
const logoutButton = document.getElementById('logout-button');
logoutButton.addEventListener('click', logout);

// Function to fetch and display all users
function getAllUsers() {
  fetch('/users')
    .then(response => response.json())
    .then(data => {
      if (Array.isArray(data)) {
        // Update the user list in the UI
        const userListElement = document.getElementById('users-list');
        userListElement.innerHTML = '';

        for (const user of data) {
          const userItem = document.createElement('li');
          userItem.textContent = user.username;
          userListElement.appendChild(userItem);
        }
      } else {
        alert('Error fetching users');
      }
    })
    .catch(error => {
      console.error(error);
      alert('Internal server error. Please try again later.');
    });
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', getAllUsers);

// Function to handle delete user confirmation
function deleteUserConfirmation() {
  const confirmation = confirm('Are you sure you want to delete your account?');

  if (confirmation) {
    fetch('/users/' + currentUserId, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    }).then(response => response.json())
      .then(data => {
        if (data.message === 'User deleted successfully') {
          localStorage.removeItem('access_token');
          window.location.href = '/';
        } else {
          alert('Error deleting user.');
        }
      })
      .catch(error => {
        console.error(error);
        alert('Internal server error. Please try again later.');
      });
  }
}

// Bind click event listener to delete button
const deleteButton = document.getElementById('delete-user-button');
deleteButton.addEventListener('click', deleteUserConfirmation);
