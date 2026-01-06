<script setup lang="ts">
import { RouterView, RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="min-h-screen bg-slate-50 pb-24">
    <!-- Header with Amber gradient -->
    <header class="fixed top-0 left-0 right-0 bg-gradient-to-r from-amber-500 to-amber-600 text-white px-4 py-3 shadow-lg z-50">
      <div class="flex items-center justify-center gap-2">
        <span class="text-2xl">☀️</span>
        <h1 class="text-xl font-bold tracking-tight">SunPaddi</h1>
      </div>
      <p class="text-amber-100 text-xs text-center mt-0.5">Your Solar Energy Companion</p>
    </header>

    <!-- Main Content -->
    <main class="pt-20 px-4 pb-4">
      <RouterView />
    </main>

    <!-- Bottom Navigation with Slate theme -->
    <nav class="fixed bottom-0 left-0 right-0 bg-slate-800 flex justify-around py-2 px-4 z-50 safe-area-bottom">
      <RouterLink 
        to="/" 
        class="flex flex-col items-center py-2 px-4 rounded-xl transition-all duration-200"
        :class="route.path === '/' ? 'bg-amber-500 text-white scale-105' : 'text-slate-400 hover:text-amber-400 active:bg-slate-700'"
      >
        <span class="text-xl mb-0.5">🏠</span>
        <span class="text-xs font-medium">Home</span>
      </RouterLink>
      <RouterLink 
        to="/calculator" 
        class="flex flex-col items-center py-2 px-4 rounded-xl transition-all duration-200"
        :class="route.path === '/calculator' ? 'bg-amber-500 text-white scale-105' : 'text-slate-400 hover:text-amber-400 active:bg-slate-700'"
      >
        <span class="text-xl mb-0.5">⚡</span>
        <span class="text-xs font-medium">Sizer</span>
      </RouterLink>
      <RouterLink 
        to="/deals" 
        class="flex flex-col items-center py-2 px-4 rounded-xl transition-all duration-200"
        :class="route.path === '/deals' ? 'bg-amber-500 text-white scale-105' : 'text-slate-400 hover:text-amber-400 active:bg-slate-700'"
      >
        <span class="text-xl mb-0.5">🛒</span>
        <span class="text-xs font-medium">Deals</span>
      </RouterLink>
    </nav>
  </div>
</template>

<style>
/* Safe area for notched phones */
.safe-area-bottom {
  padding-bottom: max(0.5rem, env(safe-area-inset-bottom));
}

/* Smooth page transitions */
.router-view-enter-active,
.router-view-leave-active {
  transition: opacity 0.2s ease;
}
.router-view-enter-from,
.router-view-leave-to {
  opacity: 0;
}
</style>
