<template>
  <div id="app">
    <Navbar />
    <template v-if="isLoggedIn">
      <router-view />
    </template>
    <template v-else>
      <Auth />
    </template>
  </div>
</template>

<script>
import Auth from './components/Auth.vue';
import { store } from './store';

export default {
  data() {
    return {
      isLoggedIn: false,
    };
  },
  computed: {
    user() {
      return store.state.user;
    },
  },
  created() {
    this.isLoggedIn = store.state.isLoggedIn;
  },
};
</script>

<style scoped>
...
</style>

