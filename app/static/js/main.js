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

//function retrieveData() {
//    let email = document.getElementById('login-email').value;
//    let password = document.getElementById('login-password').value;

//    let user_records = JSON.parse(localStorage.getItem('users')) || [];

//    let user = user_records.find((v) => v.email === email && v.password === password);

//    if (user) {
//        alert('Login success');
//        localStorage.setItem('current_user', JSON.stringify(user));
//        localStorage.setItem('username', user.username);
//        localStorage.setItem('email', user.email);
//        window.location.href = '/dashboard';
//    } else {
//        alert('Login failed');
//    }
//}
//

async function retrieveData() {
    let email = document.getElementById('login-email').value;
    let password = document.getElementById('login-password').value;

    // Send user login data to the server
    try {
        let response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password,
            }),
        });

        let data = await response.json();

        if (data.success) {
            // Save access token to localStorage
            localStorage.setItem('access_token', data.access_token);

            alert('Login success');
            window.location.href = '/dashboard';
        } else {
            alert('Login failed: ' + data.error);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred during login. Please try again.');
    }
}
