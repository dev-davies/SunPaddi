<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="space-y-5">
    <!-- Hero Card -->
    <div class="bg-gradient-to-br from-amber-500 to-orange-500 rounded-2xl p-6 text-white shadow-lg">
      <div class="flex items-center gap-3 mb-4">
        <span class="text-4xl">☀️</span>
        <div>
          <h2 class="text-xl font-bold">Welcome to SunPaddi</h2>
          <p class="text-amber-100 text-sm">Your solar energy companion</p>
        </div>
      </div>
      <p class="text-white/90 text-sm mb-4">
        Size your solar system, find the best deals, and say goodbye to "NEPA" wahala!
      </p>
      <RouterLink 
        to="/calculator" 
        class="inline-flex items-center gap-2 bg-white text-amber-600 font-bold px-5 py-3 rounded-xl hover:bg-amber-50 active:scale-95 transition-all"
      >
        <span>⚡</span>
        Start Sizing
      </RouterLink>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-2 gap-3">
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-2xl">💰</span>
          <span class="text-xs text-slate-500 uppercase tracking-wide font-medium">Monthly Savings</span>
        </div>
        <span class="block text-2xl font-bold text-slate-800">₦0</span>
        <span class="text-xs text-slate-400">vs. generator</span>
      </div>
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-100">
        <div class="flex items-center gap-2 mb-2">
          <span class="text-2xl">🌍</span>
          <span class="text-xs text-slate-500 uppercase tracking-wide font-medium">Carbon Offset</span>
        </div>
        <span class="block text-2xl font-bold text-green-600">0 kg</span>
        <span class="text-xs text-slate-400">CO₂ reduced</span>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
      <h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2">
        <span>🚀</span>
        Quick Actions
      </h3>
      <div class="space-y-3">
        <RouterLink 
          to="/calculator" 
          class="flex items-center gap-4 p-4 bg-slate-50 rounded-xl hover:bg-slate-100 active:bg-slate-200 transition-all"
        >
          <div class="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center text-2xl">
            ⚡
          </div>
          <div class="flex-1">
            <span class="font-semibold text-slate-800 block">Size My System</span>
            <span class="text-sm text-slate-500">Calculate your solar needs</span>
          </div>
          <span class="text-slate-400">→</span>
        </RouterLink>
        
        <RouterLink 
          to="/deals" 
          class="flex items-center gap-4 p-4 bg-slate-50 rounded-xl hover:bg-slate-100 active:bg-slate-200 transition-all"
        >
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center text-2xl">
            🛒
          </div>
          <div class="flex-1">
            <span class="font-semibold text-slate-800 block">Browse Deals</span>
            <span class="text-sm text-slate-500">Find the best prices</span>
          </div>
          <span class="text-slate-400">→</span>
        </RouterLink>
      </div>
    </div>

    <!-- Nigerian Context Banner -->
    <div class="bg-gradient-to-r from-slate-700 to-slate-800 rounded-2xl p-5 text-white">
      <div class="flex items-center gap-3">
        <span class="text-3xl">🇳🇬</span>
        <div>
          <p class="font-semibold">Built for Nigeria</p>
          <p class="text-slate-300 text-sm">Prices in Naira • Local vendors • Real-time deals</p>
        </div>
      </div>
    </div>
  </div>
</template>
