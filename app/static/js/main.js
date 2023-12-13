function loginFormSubmit(event) {
  event.preventDefault();

  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  }).then(response => response.json())
    .then(data => {
      if (data.message === 'Login successful') {
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

function registerFormSubmit(event) {
  event.preventDefault();

  const username = document.getElementById('register-username').value;
  const email = document.getElementById('register-email').value;
  const password = document.getElementById('register-password').value;

  fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username,
      email: email,
      password: password
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
// const logoutButton = document.getElementById('logout-button');
// logoutButton.addEventListener('click', logout);

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
