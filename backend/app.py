from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from services import calculate_solar_needs

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sunpaddi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # panel, battery, inverter
    specs = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    vendor_url = db.Column(db.String(500), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class Appliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    default_watts = db.Column(db.Integer, nullable=False)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_phone = db.Column(db.String(20), nullable=False)
    system_recommended = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return 'SunPaddi API is live'

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    appliances = data.get('appliances', [])
    if not appliances:
        return jsonify({"error": "No appliances list provided"}), 400
        
    try:
        result = calculate_solar_needs(appliances)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
