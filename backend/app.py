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

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the SunPaddi Backend!",
        "status": "active"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
