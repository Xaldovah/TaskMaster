function retrieveData(event) {
    event.preventDefault(); // Prevent form submission

    let email, password;
    email = document.getElementById("login-email").value;
    password = document.getElementById("login-password").value;

    let user_records = JSON.parse(localStorage.getItem("users")) || [];

    if (user_records.some((v) => v.email === email && v.password === password)) {
        alert("Login Successful");

        // Get the current user
        let current_user = user_records.filter((v) => v.email === email && v.password === password)[0];

        // Save user details in localStorage
        localStorage.setItem("name", current_user.name);
        localStorage.setItem("email", current_user.email);

        // Redirect to the dashboard
        window.location.href = "dashboard.html";
    } else {
        alert("Login Failed. Please check your email and password.");
    }
}

var card = document.getElementById("card");

function openRegister() {
	card.style.transform = "rotateY(-180deg)";
}

function openLogin(){
	card.style.transform = "rotateY(0deg)";
}

function saveData() {
    // Get user input
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;

    // Basic validation
    if (!name || !email || !password) {
        alert("Please fill in all fields.");
        return;
    }

    // Check for duplicate email
    if (isDuplicateEmail(email)) {
        alert("Duplicate email. Please use a different email address.");
        return;
    }

    // Hash the password
    bcrypt.hash(password, 10, function(err, hash) {
        if (err) {
            console.error("Error hashing password:", err);
            alert("Internal server error. Please try again later.");
            return;
        }

        // Save user data with hashed password
        let user_records = getUserRecords();
        user_records.push({
            "name": name,
            "email": email,
            "password": hash  // Store the hashed password
        });
        localStorage.setItem("users", JSON.stringify(user_records));

        alert("User data saved successfully!");
    });
}

function isDuplicateEmail(email) {
    let user_records = getUserRecords();
    return user_records.some((user) => user.email === email);
}

function getUserRecords() {
    return JSON.parse(localStorage.getItem("users")) || [];
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
