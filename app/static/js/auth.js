new Vue({
	el: '#auth',
	data: {
		username: '',
		email: '',
		password: '',
		message: '' ,
	},

	methods: {
		async register() {
			try {
				const response = await fetch('/register', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						username: this.username,
						email: this.email,
						password: this.password,
					}),
				});

				const data = await response.json();

				if (response.ok) {
					this.message = 'Registration successful!';
				} else {
					this.message = data.error || 'Registration failed';
				}
			} catch (error) {
				console.error('Error during registration:', error);
			}
		},
		
		async login() {
			try {
				const response = await fetch('/login', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({
						email: this.email,
						password: this.password,
					}),
				});

				const data = await response.json();

				if (response.ok) {
					this.message = 'Login successful!';
				} else {
					this.message = data.error || 'Login failed';
				}
			} catch (error) {
				console.error('Error during login:', error);
			}
		},
	},
});
