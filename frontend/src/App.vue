<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 bg-amber-500 text-white p-4 shadow-md z-50">
      <h1 class="text-xl font-bold text-center">SunPaddi</h1>
    </header>

    <!-- Main Content -->
    <main class="pt-20 px-4">
      <RouterView />
    </main>

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 flex justify-around p-3 z-50">
      <RouterLink to="/" class="flex flex-col items-center text-gray-600 hover:text-amber-500 active:text-amber-500">
        <span class="text-xs mt-1">Home</span>
      </RouterLink>
      <RouterLink to="/calculator" class="flex flex-col items-center text-gray-600 hover:text-amber-500 active:text-amber-500">
        <span class="text-xs mt-1">Calculator</span>
      </RouterLink>
      <RouterLink to="/deals" class="flex flex-col items-center text-gray-600 hover:text-amber-500 active:text-amber-500">
        <span class="text-xs mt-1">Deals</span>
      </RouterLink>
    </nav>
  </div>
</template>

<style>
/* Add any specific overrides if needed, mostly doing Tailwind */
</style>
