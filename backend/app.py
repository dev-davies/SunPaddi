from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from models import db, Product, Appliance, Lead

app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sunpaddi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db.init_app(app)

# Enable CORS for the Vue.js frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

with app.app_context():
    db.create_all()

@app.route('/api/update-prices', methods=['GET'])
def update_prices():
    try:
        from scraper import run_scraper
        results = run_scraper()
        return jsonify({
            "message": "Prices updated successfully",
            "count": len(results),
            "data": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    # Sort by is_sponsored desc (True first), then name
    products = Product.query.order_by(Product.is_sponsored.desc(), Product.name.asc()).all()
    return jsonify([p.to_dict() for p in products])

from flask import request
@app.route('/api/lead', methods=['POST'])
def create_lead():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('phone'):
        return jsonify({"error": "Name and Phone are required"}), 400
    
    try:
        new_lead = Lead(
            name=data['name'],
            email=data.get('email'),
            phone=data['phone'],
            energy_needs=data.get('energy_needs')
        )
        db.session.add(new_lead)
        db.session.commit()
        return jsonify({"message": "Lead submitted successfully", "id": new_lead.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/calculate', methods=['POST'])
def calculate_system():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    total_watts = data.get('totalWatts', 0)
    night_hours = data.get('nightHours', 8)
    appliances = data.get('appliances', [])
    
    # Calculate energy needed (Wh)
    energy_wh = total_watts * night_hours
    
    # Add 20% buffer for inefficiency
    energy_with_buffer = energy_wh * 1.2
    
    # Battery sizing (assuming 12V 200Ah = 2.4kWh, 50% DoD)
    battery_kwh = energy_with_buffer / 1000
    batteries_needed = max(1, int(battery_kwh / 1.2) + 1)  # 1.2kWh usable per battery
    
    # Inverter sizing (add 25% headroom)
    inverter_watts = total_watts * 1.25
    inverter_kva = round(inverter_watts / 800, 1)  # Rough conversion
    inverter_kva = max(1.5, inverter_kva)  # Minimum 1.5kVA
    
    # Panel sizing (assuming 5 peak sun hours, 550W panels)
    daily_generation_needed = energy_with_buffer / 1000  # kWh
    panel_watts_needed = (daily_generation_needed / 5) * 1000 * 1.3  # 30% losses
    panels_550w = max(1, int(panel_watts_needed / 550) + 1)
    
    return jsonify({
        "success": True,
        "input": {
            "totalWatts": total_watts,
            "nightHours": night_hours,
            "applianceCount": len([a for a in appliances if a.get('quantity', 0) > 0])
        },
        "recommendation": {
            "inverterKva": inverter_kva,
            "batteries": batteries_needed,
            "panels": panels_550w,
            "batteryKwh": round(battery_kwh, 2),
            "dailyEnergyKwh": round(energy_with_buffer / 1000, 2)
        }
    })

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the SunPaddi Backend!",
        "status": "active"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
