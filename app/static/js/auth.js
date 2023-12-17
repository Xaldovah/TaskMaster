new Vue({
    el: '#auth',
    data: {
        username: '',
        email: '',
        password: '',
        message: '',
    },
    methods: {
        register() {
            fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    email: this.email,
                    password: this.password,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.message = 'Registration successful!';
                    } else {
                        this.message = data.error || 'Registration failed';
                    }
                })
                .catch(error => {
                    console.error('Error during registration:', error);
                });
        },
        login() {
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: this.email,
                    password: this.password,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.message = 'Login successful!';
                    } else {
                        this.message = data.error || 'Login failed';
                    }
                })
                .catch(error => {
                    console.error('Error during login:', error);
                });
        },
    },
});
