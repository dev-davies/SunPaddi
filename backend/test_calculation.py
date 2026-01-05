import requests
import json

def test_calculate():
    url = "http://localhost:5000/api/calculate"
    
    # Sample payload
    # 2 Fans (75W each) for 8 hours
    # 5 LEDs (10W each) for 6 hours
    # 1 TV (120W) for 4 hours
    payload = {
        "appliances": [
            {"watts": 75, "quantity": 2, "hours": 8},
            {"watts": 10, "quantity": 5, "hours": 6},
            {"watts": 120, "quantity": 1, "hours": 4}
        ]
    }
    
    # Manual Calculation Check:
    # Fans: 75 * 2 = 150W. 150 * 8 = 1200Wh
    # LEDs: 10 * 5 = 50W. 50 * 6 = 300Wh
    # TV: 120 * 1 = 120W. 120 * 4 = 480Wh
    # Total Peak Load = 150 + 50 + 120 = 320W
    # Total Daily Wh = 1200 + 300 + 480 = 1980Wh
    
    # Rules:
    # 1. Safety Factor 1.2 => Required Wh = 1980 * 1.2 = 2376Wh
    # 2. Inverter: Peak(320) * 1.25 / 0.8 => 320 * 1.5625 = 500W -> 0.5 kVA
    # 3. Panels (550W, 4.5 sun hours): 2376 / (550 * 4.5) = 2376 / 2475 = 0.96 => 1 Panel
    # 4. Batteries (200Ah, 12V, 50% DoD): 2376 / (12 * 200 * 0.5) = 2376 / 1200 = 1.98 => 2 Batteries
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print("Scenerio: 2 Fans (8h), 5 LEDs (6h), 1 TV (4h)")
        print(json.dumps(result, indent=2))
        
        # Simple assertions based on manual calculation above
        assert result['total_daily_wh'] == 2376.0, f"Expected 2376.0, got {result['total_daily_wh']}"
        assert result['total_peak_load'] == 320, f"Expected 320, got {result['total_peak_load']}"
        assert result['recommended_inverter_kva'] == 0.5, f"Expected 0.5, got {result['recommended_inverter_kva']}"
        assert result['number_of_panels_550w'] == 1, f"Expected 1, got {result['number_of_panels_550w']}"
        assert result['number_of_batteries_200ah_12v'] == 2, f"Expected 2, got {result['number_of_batteries_200ah_12v']}"
        
        print("\n✅ Verification PASSED")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to server. Is it running?")
    except AssertionError as ae:
        print(f"\n❌ Verification FAILED: {ae}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_calculate()
