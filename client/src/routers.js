import { createRouter, createWebHistory } from 'vue-router';
import Auth from '../components/Auth.vue';

const routes = [
  { path: '/', redirect: 'https://arkwebs.tech/login' },
  { path: 'https://arkwebs.tech/login', component: Auth },
  { path: 'https://arkwebs.tech/register', component: Auth },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
