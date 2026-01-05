<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useSizerStore } from '@/stores/sizer'

const store = useSizerStore()

const loading = ref(false)
const results = ref<any>(null)
const products = ref<any[]>([])
const showResults = ref(false)

async function generateQuote() {
  loading.value = true
  try {
    const payload = {
      totalWatts: store.totalWatts,
      nightHours: store.nightHours,
      appliances: store.appliances.filter(a => a.quantity > 0).map(a => ({
        name: a.name,
        watts: a.watts,
        quantity: a.quantity
      }))
    }
    
    const response = await axios.post('/api/calculate', payload)
    results.value = response.data.recommendation
    showResults.value = true
    
    // Fetch products for deals section
    const productsRes = await axios.get('/api/products')
    products.value = productsRes.data
  } catch (error) {
    console.error('Calculation failed:', error)
  } finally {
    loading.value = false
  }
}

function shareOnWhatsApp() {
  const selected = store.appliances.filter(a => a.quantity > 0)
  const appList = selected.map(a => `${a.quantity}x ${a.name}`).join(', ')
  
  const text = `🌞 *My SunPaddi Solar Quote*\n\n` +
    `📱 Appliances: ${appList}\n` +
    `⏰ Runtime: ${store.nightHours} hours\n\n` +
    `⚡ Recommended System:\n` +
    `• Inverter: ${results.value?.inverterKva} kVA\n` +
    `• Batteries: ${results.value?.batteries} units\n` +
    `• Solar Panels: ${results.value?.panels}x 550W\n\n` +
    `Get your free quote at sunpaddi.ng`
  
  const url = `https://wa.me/?text=${encodeURIComponent(text)}`
  window.open(url, '_blank')
}

onMounted(() => {
  // Pre-fetch products
  axios.get('/api/products').then(res => products.value = res.data).catch(() => {})
})
</script>

<template>
  <div class="space-y-6">
    <!-- Generate Quote Button -->
    <button 
      @click="generateQuote"
      :disabled="loading || store.totalWatts === 0"
      class="w-full bg-gradient-to-r from-amber-500 to-orange-500 text-white font-semibold py-4 rounded-xl hover:from-amber-600 hover:to-orange-600 active:scale-[0.98] transition-all shadow-lg shadow-amber-500/30 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
    >
      <span v-if="loading" class="animate-spin">⏳</span>
      <span v-else>⚡</span>
      {{ loading ? 'Calculating...' : 'Generate Quote' }}
    </button>

    <!-- Energy Blueprint Card -->
    <div v-if="showResults && results" class="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl p-6 text-white">
      <div class="flex items-center gap-2 mb-4">
        <span class="text-2xl">📋</span>
        <h3 class="text-lg font-bold">Your Energy Blueprint</h3>
      </div>

      <div class="grid grid-cols-3 gap-3 mb-4">
        <div class="bg-white/20 backdrop-blur rounded-xl p-3 text-center">
          <span class="text-3xl block mb-1">🔌</span>
          <span class="text-2xl font-bold block">{{ results.inverterKva }}</span>
          <span class="text-xs opacity-80">kVA Inverter</span>
        </div>
        <div class="bg-white/20 backdrop-blur rounded-xl p-3 text-center">
          <span class="text-3xl block mb-1">🔋</span>
          <span class="text-2xl font-bold block">{{ results.batteries }}</span>
          <span class="text-xs opacity-80">Batteries</span>
        </div>
        <div class="bg-white/20 backdrop-blur rounded-xl p-3 text-center">
          <span class="text-3xl block mb-1">☀️</span>
          <span class="text-2xl font-bold block">{{ results.panels }}</span>
          <span class="text-xs opacity-80">550W Panels</span>
        </div>
      </div>

      <div class="text-sm opacity-90 text-center">
        Daily Energy: {{ results.dailyEnergyKwh }} kWh | Battery Capacity: {{ results.batteryKwh }} kWh
      </div>
    </div>

    <!-- Best Deals Section -->
    <div v-if="showResults && products.length > 0" class="bg-white rounded-2xl p-5 shadow-sm border border-gray-100">
      <div class="flex items-center gap-2 mb-4">
        <span class="text-xl">🔥</span>
        <h3 class="font-bold text-gray-800">Best Deals Near You</h3>
      </div>

      <div class="space-y-3">
        <div 
          v-for="product in products.slice(0, 5)" 
          :key="product.id"
          class="flex items-center gap-3 p-3 rounded-xl transition-all"
          :class="product.is_sponsored ? 'bg-amber-50 border-2 border-amber-300' : 'bg-gray-50'"
        >
          <div class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center text-2xl">
            {{ product.category === 'solar_panel' ? '☀️' : product.category === 'battery' ? '🔋' : '⚡' }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="font-medium text-gray-800 truncate">{{ product.name }}</span>
              <span v-if="product.is_sponsored" class="px-2 py-0.5 bg-amber-500 text-white text-xs rounded-full font-medium">Partner</span>
            </div>
            <span class="text-sm text-gray-500">{{ product.category }}</span>
          </div>
          <div class="text-right">
            <span class="font-bold text-gray-800">₦{{ product.price?.toLocaleString() }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- WhatsApp Share Button -->
    <button 
      v-if="showResults"
      @click="shareOnWhatsApp"
      class="w-full bg-green-500 text-white font-semibold py-4 rounded-xl hover:bg-green-600 active:scale-[0.98] transition-all flex items-center justify-center gap-2"
    >
      <span class="text-xl">📱</span>
      Share on WhatsApp
    </button>
  </div>
</template>
