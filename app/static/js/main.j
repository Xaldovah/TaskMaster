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
