async function registerUser() {
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    // Hash the password before sending it to the server
    let hashedPassword = await hashPassword(password);

    // Send user registration data to the server
    try {
        let response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: hashedPassword,
            }),
        });

        let data = await response.json();

        if (data.success) {
            alert('Registration successful');
            window.location.href = '/login';
        } else {
            alert('Registration failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occurred during registration. Please try again.');
    }
}

async function hashPassword(password) {
    // Send the password to the server for hashing
    try {
        let response = await fetch('/hash_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password }),
        });

        let data = await response.json();

        if (data.success) {
            return data.hashedPassword;
        } else {
            throw new Error('Password hashing failed');
        }
    } catch (error) {
        console.error('Error during password hashing:', error);
        throw new Error('Password hashing failed');
    }
}

async function loginUser() {
    let email = document.getElementById('login-email').value;
    let password = document.getElementById('login-password').value;

    // Hash the password before sending it to the server
    let hashedPassword = await hashPassword(password);

    // Send login data to the server
    try {
        let response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: hashedPassword,
            }),
        });

        let data = await response.json();

        if (data.success) {
            alert('Login successful');
            // Handle the success, for example, redirect to the dashboard
            window.location.href = '/dashboard';
        } else {
            alert('Login failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login. Please try again.');
    }
}
