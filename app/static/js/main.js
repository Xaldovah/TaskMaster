function saveData() {
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    let user_records = JSON.parse(localStorage.getItem('users')) || [];
    if (user_records.some((v) => v.email == email)) {
        alert('Email already exists');
    } else {
        user_records.push({
            "username": username,
            "email": email,
            "password": password
        });
        localStorage.setItem('users', JSON.stringify(user_records));
        alert('Data saved successfully');
        window.location.href = '/login';
    }
}

function retrieveData() {
    let email = document.getElementById('login-email').value;
    let password = document.getElementById('login-password').value;

    let user_records = JSON.parse(localStorage.getItem('users')) || [];

    const encoder = new TextEncoder();
    const passwordBuffer = encoder.encode(password);
    const hashedPasswordBuffer = await crypto.subtle.digest('SHA-256', passwordBuffer);
    const hashedPassword = Array.from(new Uint8Array(hashedPasswordBuffer)).map(byte => byte.toString(16).padStart(2, '0')).join('');

    let user = user_records.find((v) => v.email === email && v.password === hashedpassword);

    if (user) {
	let accessToken = generateAccessToken();

	localStorage.setItem('access_token', accessToken);
        localStorage.setItem('current_user', JSON.stringify(user));
        localStorage.setItem('username', user.username);
        localStorage.setItem('email', user.email);

	alert('Login success');
        window.location.href = '/dashboard';
    } else {
        alert('Login failed');
    }
}

// Function to generate a simple access token
function generateAccessToken() {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}
