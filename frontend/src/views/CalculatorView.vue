<script setup lang="ts">
import { useSizerStore } from '@/stores/sizer'
import SizingResult from '@/components/SizingResult.vue'

const store = useSizerStore()
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="text-center">
      <h2 class="text-2xl font-bold text-gray-800">Solar Sizer</h2>
      <p class="text-gray-500 text-sm mt-1">Select your appliances to calculate your needs</p>
    </div>

    <!-- Appliance Grid -->
    <div class="grid grid-cols-2 gap-3">
      <div 
        v-for="appliance in store.appliances" 
        :key="appliance.id"
        class="bg-white rounded-2xl p-4 shadow-sm border border-gray-100 transition-all duration-200"
        :class="{ 'ring-2 ring-amber-400 bg-amber-50': appliance.quantity > 0 }"
      >
        <div class="text-center mb-3">
          <span class="text-3xl">{{ appliance.icon }}</span>
          <p class="font-medium text-gray-800 mt-1">{{ appliance.name }}</p>
          <p class="text-xs text-gray-400">{{ appliance.watts }}W</p>
        </div>
        
        <div class="flex items-center justify-center gap-3">
          <button 
            @click="store.decrement(appliance.id)"
            class="w-9 h-9 rounded-full bg-gray-100 text-gray-600 font-bold text-lg flex items-center justify-center hover:bg-gray-200 active:scale-95 transition-all"
            :disabled="appliance.quantity === 0"
            :class="{ 'opacity-40': appliance.quantity === 0 }"
          >
            −
          </button>
          <span class="text-xl font-bold text-gray-800 w-8 text-center">{{ appliance.quantity }}</span>
          <button 
            @click="store.increment(appliance.id)"
            class="w-9 h-9 rounded-full bg-amber-500 text-white font-bold text-lg flex items-center justify-center hover:bg-amber-600 active:scale-95 transition-all"
          >
            +
          </button>
        </div>
      </div>
    </div>

    <!-- Night Hours Slider -->
    <div class="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-5 text-white">
      <div class="flex justify-between items-center mb-3">
        <span class="font-medium">Night Hours</span>
        <span class="text-2xl font-bold">{{ store.nightHours }}h</span>
      </div>
      <input 
        type="range" 
        v-model.number="store.nightHours" 
        min="1" 
        max="24" 
        class="w-full h-2 bg-white/30 rounded-lg appearance-none cursor-pointer accent-white"
      />
      <div class="flex justify-between text-xs text-white/70 mt-1">
        <span>1h</span>
        <span>24h</span>
      </div>
    </div>

    <!-- Results Summary -->
    <div class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
      <h3 class="font-semibold text-gray-800 mb-4">Your Solar Requirements</h3>
      
      <div class="space-y-3">
        <div class="flex justify-between items-center">
          <span class="text-gray-500">Total Power Load</span>
          <span class="font-bold text-gray-800">{{ store.totalWatts }} W</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-gray-500">Energy Needed ({{ store.nightHours }}h)</span>
          <span class="font-bold text-gray-800">{{ store.totalWattHours }} Wh</span>
        </div>
        <div class="h-px bg-gray-100"></div>
        <div class="flex justify-between items-center">
          <span class="text-gray-600 font-medium">Recommended Battery</span>
          <span class="text-xl font-bold text-amber-600">{{ store.recommendedBatteryKWh }} kWh</span>
        </div>
      </div>
    </div>

    <!-- Sizing Result Component -->
    <SizingResult />
  </div>
</template>
