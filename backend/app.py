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

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to the SunPaddi Backend!",
        "status": "active"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
