<script setup lang="ts">
import { ref } from 'vue'

const message = ref('Welcome to SunPaddi')
</script>

<template>
  <div class="space-y-4">
    <div class="bg-white p-6 rounded-lg shadow-sm">
      <h2 class="text-lg font-semibold text-gray-800 mb-2">{{ message }}</h2>
      <p class="text-gray-600">Your solar energy companion.</p>
    </div>
    
    <div class="grid grid-cols-2 gap-4">
      <div class="bg-blue-50 p-4 rounded-lg text-center">
        <span class="block text-2xl font-bold text-blue-600">0</span>
        <span class="text-sm text-gray-600">Saved (N)</span>
      </div>
      <div class="bg-green-50 p-4 rounded-lg text-center">
        <span class="block text-2xl font-bold text-green-600">0%</span>
        <span class="text-sm text-gray-600">Carbon Offset</span>
      </div>
    </div>
  </div>
</template>
