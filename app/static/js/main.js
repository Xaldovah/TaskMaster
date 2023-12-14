function saveAndTestUser() {
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  fetch('/register', {
    method: 'POST',
    body: JSON.stringify({ name, email, password })
  }).then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log('User registered successfully!');
      } else {
        console.error('Registration failed:', data.error);
      }
    });
}

const loginForm = document.querySelector('.login-form');
loginForm.addEventListener('submit', function(event) {
  event.preventDefault();

  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  // Send POST request to login endpoint
  fetch('/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  }).then(response => response.json())
    .then(data => {
      if (data.success) {
        // Login successful
        // Redirect to desired page
        window.location.href = url_for('dashboard');
      } else {
        // Display error message
        flash(data.error, 'danger');
      }
    });
});

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
