from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # solar_panel, battery, inverter, controller
    specs = db.Column(db.JSON, nullable=True) # generic JSON for varying specs
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    is_sponsored = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'specs': self.specs,
            'price': self.price,
            'stock': self.stock,
            'is_sponsored': self.is_sponsored
        }

class Appliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    watts = db.Column(db.Float, nullable=False) # typical power consumption in watts

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'watts': self.watts
        }

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    energy_needs = db.Column(db.Text, nullable=True) # Text description or JSON of needs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'energy_needs': self.energy_needs,
            'created_at': self.created_at.isoformat()
        }
