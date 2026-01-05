import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import './assets/main.css'
import App from './App.vue'
import HomeView from './views/HomeView.vue'
import CalculatorView from './views/CalculatorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/calculator',
      name: 'calculator',
      component: CalculatorView
    },
    {
      path: '/deals',
      name: 'deals',
      component: HomeView // Placeholder
    }
  ]
})

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
