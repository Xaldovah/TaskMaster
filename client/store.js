import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    isLoggedIn: false, // User login status
    user: {}, // User object with information (optional)
    token: '', // Authentication token (if using JWT)
  },
  mutations: {
    LOGIN(state, payload) {
      state.isLoggedIn = true;
      state.user = payload.user; // Update user information
      state.token = payload.token; // Store token (if applicable)
    },
    LOGOUT(state) {
      state.isLoggedIn = false;
      state.user = {}; // Clear user information
      state.token = ''; // Clear token
    },
  },
  actions: {
    async login(context, payload) {
      // Send login request to your backend API
      // Use payload for login credentials
      // Replace with your specific API call and handle response
      const response = await fetch('/api/login', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (data.success) {
        context.commit('LOGIN', {
          user: data.user, // Extract user information from response
          token: data.token, // Extract token from response (if applicable)
        });
      } else {
        // Handle login failure
        console.error('Login failed:', data.error);
      }
    },
    async logout(context) {
      // Send logout request to your backend API (if needed)
      // Replace with your specific API call and handle response
      // context.commit('LOGOUT'); // Logout even if API call fails
    },
  },
});

export default store;
