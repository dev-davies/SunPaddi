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
      class="w-full bg-gradient-to-r from-amber-500 to-amber-600 text-white font-bold py-4 rounded-2xl transition-all duration-200 shadow-lg shadow-amber-500/30 flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
      :class="{ 
        'hover:from-amber-600 hover:to-amber-700 active:scale-[0.97] active:shadow-amber-500/50': !loading && store.totalWatts > 0 
      }"
    >
      <!-- Rotating Sun Spinner -->
      <span v-if="loading" class="sun-spinner text-2xl">☀️</span>
      <span v-else class="text-xl">⚡</span>
      <span class="text-lg">{{ loading ? 'Sizing Your System...' : 'Generate Quote' }}</span>
    </button>

    <!-- Energy Blueprint Card -->
    <div v-if="showResults && results" class="bg-gradient-to-br from-slate-700 to-slate-800 rounded-2xl p-6 text-white shadow-xl">
      <div class="flex items-center gap-3 mb-5">
        <div class="w-10 h-10 bg-amber-500 rounded-xl flex items-center justify-center">
          <span class="text-xl">📋</span>
        </div>
        <div>
          <h3 class="text-lg font-bold">Your Energy Blueprint</h3>
          <p class="text-slate-400 text-xs">Personalized solar recommendation</p>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-3 mb-5">
        <div class="bg-slate-600/50 backdrop-blur rounded-xl p-4 text-center border border-slate-500/30">
          <span class="text-3xl block mb-2">🔌</span>
          <span class="text-2xl font-bold text-amber-400 block">{{ results.inverterKva }}</span>
          <span class="text-xs text-slate-300">kVA Inverter</span>
        </div>
        <div class="bg-slate-600/50 backdrop-blur rounded-xl p-4 text-center border border-slate-500/30">
          <span class="text-3xl block mb-2">🔋</span>
          <span class="text-2xl font-bold text-amber-400 block">{{ results.batteries }}</span>
          <span class="text-xs text-slate-300">Batteries</span>
        </div>
        <div class="bg-slate-600/50 backdrop-blur rounded-xl p-4 text-center border border-slate-500/30">
          <span class="text-3xl block mb-2">☀️</span>
          <span class="text-2xl font-bold text-amber-400 block">{{ results.panels }}</span>
          <span class="text-xs text-slate-300">550W Panels</span>
        </div>
      </div>

      <div class="bg-slate-600/30 rounded-xl p-3 text-center">
        <span class="text-slate-300 text-sm">
          Daily: <span class="text-amber-400 font-semibold">{{ results.dailyEnergyKwh }} kWh</span> • 
          Storage: <span class="text-amber-400 font-semibold">{{ results.batteryKwh }} kWh</span>
        </span>
      </div>
    </div>

    <!-- Best Deals Section - Native looking Partner ads -->
    <div v-if="showResults && products.length > 0" class="bg-white rounded-2xl p-5 shadow-sm border border-slate-200">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-2">
          <span class="text-xl">🛒</span>
          <h3 class="font-bold text-slate-800">Recommended Products</h3>
        </div>
        <span class="text-xs text-slate-400">From trusted vendors</span>
      </div>

      <div class="space-y-3">
        <div 
          v-for="product in products.slice(0, 5)" 
          :key="product.id"
          class="flex items-center gap-3 p-3 rounded-xl transition-all duration-200 cursor-pointer"
          :class="product.is_sponsored 
            ? 'bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 hover:border-amber-300' 
            : 'bg-slate-50 hover:bg-slate-100 border border-transparent'"
        >
          <div 
            class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0"
            :class="product.is_sponsored ? 'bg-amber-100' : 'bg-slate-200'"
          >
            {{ product.category === 'solar_panel' ? '☀️' : product.category === 'battery' ? '🔋' : '⚡' }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-medium text-slate-800 truncate">{{ product.name }}</span>
              <span 
                v-if="product.is_sponsored" 
                class="px-2 py-0.5 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-[10px] rounded-full font-semibold uppercase tracking-wide"
              >
                Verified
              </span>
            </div>
            <span class="text-xs text-slate-500 capitalize">{{ product.category?.replace('_', ' ') }}</span>
          </div>
          <div class="text-right flex-shrink-0">
            <span class="font-bold text-slate-800">₦{{ product.price?.toLocaleString() }}</span>
            <p v-if="product.is_sponsored" class="text-[10px] text-amber-600">Best price</p>
          </div>
        </div>
      </div>
    </div>

    <!-- WhatsApp Share Button -->
    <button 
      v-if="showResults"
      @click="shareOnWhatsApp"
      class="w-full bg-[#25D366] text-white font-bold py-4 rounded-2xl hover:bg-[#20BD5A] active:scale-[0.97] active:bg-[#1DA851] transition-all duration-200 flex items-center justify-center gap-3 shadow-lg shadow-green-500/20"
    >
      <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
      </svg>
      <span class="text-lg">Share on WhatsApp</span>
    </button>
  </div>
</template>

<style scoped>
/* Rotating Sun Spinner */
.sun-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
