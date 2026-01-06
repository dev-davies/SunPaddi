<script setup lang="ts">
import { useSizerStore } from '@/stores/sizer'
import SizingResult from '@/components/SizingResult.vue'

const store = useSizerStore()
</script>

<template>
  <div class="space-y-5">
    <!-- Page Header -->
    <div class="text-center mb-2">
      <h2 class="text-2xl font-bold text-slate-800">Solar Sizer</h2>
      <p class="text-slate-500 text-sm">Select your appliances to calculate your needs</p>
    </div>

    <!-- Appliance Grid -->
    <div class="grid grid-cols-2 gap-3">
      <div 
        v-for="appliance in store.appliances" 
        :key="appliance.id"
        class="bg-white rounded-2xl p-4 shadow-sm border transition-all duration-200"
        :class="appliance.quantity > 0 
          ? 'ring-2 ring-amber-400 border-amber-200 bg-amber-50/50' 
          : 'border-slate-100 hover:border-slate-200'"
      >
        <div class="text-center mb-3">
          <span class="text-3xl block">{{ appliance.icon }}</span>
          <p class="font-semibold text-slate-800 mt-1">{{ appliance.name }}</p>
          <p class="text-xs text-slate-400">{{ appliance.watts }}W</p>
        </div>
        
        <div class="flex items-center justify-center gap-3">
          <button 
            @click="store.decrement(appliance.id)"
            class="w-10 h-10 rounded-full bg-slate-100 text-slate-600 font-bold text-lg flex items-center justify-center transition-all duration-150"
            :disabled="appliance.quantity === 0"
            :class="appliance.quantity === 0 
              ? 'opacity-40 cursor-not-allowed' 
              : 'hover:bg-slate-200 active:bg-slate-300 active:scale-90'"
          >
            −
          </button>
          <span 
            class="text-xl font-bold w-8 text-center"
            :class="appliance.quantity > 0 ? 'text-amber-600' : 'text-slate-400'"
          >
            {{ appliance.quantity }}
          </span>
          <button 
            @click="store.increment(appliance.id)"
            class="w-10 h-10 rounded-full bg-amber-500 text-white font-bold text-lg flex items-center justify-center hover:bg-amber-600 active:bg-amber-700 active:scale-90 transition-all duration-150 shadow-md shadow-amber-500/20"
          >
            +
          </button>
        </div>
      </div>
    </div>

    <!-- Night Hours Slider - Slate theme -->
    <div class="bg-gradient-to-br from-slate-700 to-slate-800 rounded-2xl p-5 text-white shadow-lg">
      <div class="flex justify-between items-center mb-3">
        <div class="flex items-center gap-2">
          <span class="text-xl">🌙</span>
          <span class="font-medium">Backup Hours</span>
        </div>
        <span class="text-2xl font-bold text-amber-400">{{ store.nightHours }}h</span>
      </div>
      <input 
        type="range" 
        v-model.number="store.nightHours" 
        min="1" 
        max="24" 
        class="w-full h-2 bg-slate-600 rounded-lg appearance-none cursor-pointer slider-thumb"
      />
      <div class="flex justify-between text-xs text-slate-400 mt-2">
        <span>1 hour</span>
        <span>24 hours</span>
      </div>
    </div>

    <!-- Results Summary Card -->
    <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100">
      <h3 class="font-bold text-slate-800 mb-4 flex items-center gap-2">
        <span class="text-lg">📊</span>
        Live Estimate
      </h3>
      
      <div class="space-y-3">
        <div class="flex justify-between items-center">
          <span class="text-slate-500">Total Power Load</span>
          <span class="font-bold text-slate-800">{{ store.totalWatts }} W</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-slate-500">Energy Needed ({{ store.nightHours }}h)</span>
          <span class="font-bold text-slate-800">{{ store.totalWattHours.toLocaleString() }} Wh</span>
        </div>
        <div class="h-px bg-slate-100"></div>
        <div class="flex justify-between items-center">
          <span class="text-slate-700 font-medium">Recommended Battery</span>
          <span class="text-xl font-bold text-amber-600">{{ store.recommendedBatteryKWh }} kWh</span>
        </div>
      </div>
    </div>

    <!-- Sizing Result Component -->
    <SizingResult />
  </div>
</template>

<style scoped>
/* Custom slider thumb */
.slider-thumb::-webkit-slider-thumb {
  appearance: none;
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
}

.slider-thumb::-moz-range-thumb {
  width: 24px;
  height: 24px;
  background: linear-gradient(135deg, #f59e0b, #d97706);
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
}
</style>
