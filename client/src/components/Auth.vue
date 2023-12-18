<template>
  <div class="container">
    <div class="card">
      <div class="card-front" v-show="!isRegister">
        <h2>LOGIN</h2>
        <form @submit.prevent="login" class="login-form">
          <input
            type="email"
            class="input-box"
            id="login-email"
            name="email"
            placeholder="Enter Email"
            required
          />
          <input
            type="password"
            class="input-box"
            id="login-password"
            name="password"
            placeholder="Password"
            required
          />
          <button type="submit" class="submit-btn">Submit</button>
          <label>
            <input type="checkbox" />
            Remember Me
          </label>
        </form>
        <button type="button" class="btn" @click="toggleRegister">
          Are you new?
        </button>
        <a href="#">Forgot Password</a>
      </div>

      <div class="card-back" v-show="isRegister">
        <h2>REGISTER</h2>
        <form @submit.prevent="register" class="register-form">
          <input
            type="text"
            class="input-box"
            id="username"
            name="username"
            placeholder="Enter Username"
            required
          />
          <input
            type="email"
            class="input-box"
            id="email"
            name="email"
            placeholder="Enter Email"
            required
          />
          <input
            type="password"
            class="input-box"
            id="password"
            name="password"
            placeholder="Password"
            required
          />
          <button type="submit" class="submit-btn">Submit</button>
          <label>
            <input type="checkbox" />
            Remember Me
          </label>
        </form>
        <button type="button" class="btn" @click="toggleRegister">
          I have an account
        </button>
        <a href="#">Forgot Password</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isRegister: false,
      email: '', // Add the email and password data properties
      password: '',
      message: '', // Add the message data property
    };
  },
  methods: {
    toggleRegister() {
      this.isRegister = !this.isRegister;
    },
    login() {
      fetch('https://www.arkwebs.tech/login', {
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
    register() {
      fetch('https://www.arkwebs.tech/register', {
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
  },
};
</script>

<style scoped>
/* Add your CSS styles here instead of linking to external files */
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
.card {
  width: 400px;
  background-color: #fff;
  border-radius: 5px;
  padding: 20px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  transform-style: preserve-3d;
  transition: transform 0.5s ease-in-out;
}
/* ... Add remaining styles ... */
</style>
