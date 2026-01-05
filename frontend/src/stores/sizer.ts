import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Appliance {
  id: string
  name: string
  watts: number
  icon: string
  quantity: number
}

export const useSizerStore = defineStore('sizer', () => {
  const appliances = ref<Appliance[]>([
    { id: 'fridge', name: 'Fridge', watts: 150, icon: '🧊', quantity: 0 },
    { id: 'ac', name: 'AC (1.5HP)', watts: 1200, icon: '❄️', quantity: 0 },
    { id: 'fan', name: 'Fan', watts: 70, icon: '🌀', quantity: 0 },
    { id: 'tv', name: 'TV', watts: 100, icon: '📺', quantity: 0 },
    { id: 'bulb', name: 'LED Bulb', watts: 10, icon: '💡', quantity: 0 },
    { id: 'laptop', name: 'Laptop', watts: 65, icon: '💻', quantity: 0 },
  ])

  const nightHours = ref(8)

  const totalWatts = computed(() => {
    return appliances.value.reduce((sum, app) => sum + (app.watts * app.quantity), 0)
  })

  const totalWattHours = computed(() => {
    return totalWatts.value * nightHours.value
  })

  const recommendedBatteryKWh = computed(() => {
    // Add 20% buffer for efficiency losses
    return (totalWattHours.value * 1.2 / 1000).toFixed(2)
  })

  function increment(id: string) {
    const app = appliances.value.find(a => a.id === id)
    if (app) app.quantity++
  }

  function decrement(id: string) {
    const app = appliances.value.find(a => a.id === id)
    if (app && app.quantity > 0) app.quantity--
  }

  function reset() {
    appliances.value.forEach(a => a.quantity = 0)
    nightHours.value = 8
  }

  return {
    appliances,
    nightHours,
    totalWatts,
    totalWattHours,
    recommendedBatteryKWh,
    increment,
    decrement,
    reset
  }
})
