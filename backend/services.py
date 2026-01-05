import math

def calculate_solar_needs(appliances):
    """
    Calculates solar system requirements based on appliance usage.
    
    Args:
        appliances (list): List of dicts with 'watts', 'quantity', 'hours'.
                           Example: [{'watts': 100, 'quantity': 2, 'hours': 4}]
    
    Returns:
        dict: Recommended system specifications.
    """
    total_daily_wh = 0
    total_peak_load = 0
    
    for item in appliances:
        watts = item.get('watts', 0)
        quantity = item.get('quantity', 1)
        hours = item.get('hours', 0)
        
        item_total_watts = watts * quantity
        item_daily_wh = item_total_watts * hours
        
        total_peak_load += item_total_watts
        total_daily_wh += item_daily_wh
        
    # Python constants for Nigerian context
    PEAK_SUN_HOURS = 4.5
    SAFETY_FACTOR = 1.2  # 20% for dust/heat
    INVERTER_EFFICIENCY = 0.8
    INVERTER_HEADROOM = 1.25
    PANEL_WATTAGE = 550
    BATTERY_VOLTAGE = 12
    BATTERY_CAPACITY_AH = 200
    DOD = 0.5 # Depth of Discharge for lead acid/tubular batteries (standard practice)
    
    # 1. Total Daily Watt-hours with Safety Factor
    required_daily_wh = total_daily_wh * SAFETY_FACTOR
    
    # 2. Recommended Inverter kVA (Peak load * 1.25 / 0.8)
    # Result is in Watts, convert to kVA (assuming power factor ~0.8-1.0, but formula asks for this calculation)
    # The formula provided: Peak load * 1.25 / 0.8. 
    # Usually Inverter VA = Watts / PowerFactor. Here we implement the user's specific formula.
    inverter_capacity_watts_required = (total_peak_load * INVERTER_HEADROOM) / INVERTER_EFFICIENCY
    inverter_kva = inverter_capacity_watts_required / 1000
    
    # 3. Number of 550W panels needed
    # Total Energy needed / (Panel Rating * Peak Sun Hours)
    # Note: We use required_daily_wh (with safety factor) for sizing
    panel_daily_production = PANEL_WATTAGE * PEAK_SUN_HOURS
    num_panels = math.ceil(required_daily_wh / panel_daily_production)
    
    # 4. Number of 200Ah 12V batteries needed for 1 day of autonomy
    # Total Wh / (Battery Voltage * Battery Ah * DoD)
    battery_wh_capacity = BATTERY_VOLTAGE * BATTERY_CAPACITY_AH * DOD
    num_batteries = math.ceil(required_daily_wh / battery_wh_capacity)

    return {
        "total_daily_wh": round(required_daily_wh, 2),
        "total_peak_load": total_peak_load,
        "recommended_inverter_kva": round(inverter_kva, 2),
        "number_of_panels_550w": num_panels,
        "number_of_batteries_200ah_12v": num_batteries,
        "breakdown": {
            "raw_total_wh": total_daily_wh,
            "safety_margin_wh": round(required_daily_wh - total_daily_wh, 2)
        }
    }
