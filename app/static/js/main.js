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

var card = document.getElementById("card");

function openRegister() {
	card.style.transform = "rotateY(-180deg)";
}

function openLogin(){
	card.style.transform = "rotateY(0deg)";
}

function saveData() {
	let name, email, password;
        name = document.getElementById("name").value;
        email = document.getElementById("email").value;
        password = document.getElementById("password").value;

        localStorage.setItem("name", name);
        localStorage.setItem("email", email);
        localStorage.setItem("password", password);
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
