from app import app
from models import db, Appliance

def seed_appliances():
    appliances_data = [
        {"name": "1.5HP AC", "watts": 1200},
        {"name": "Deep Freezer", "watts": 200},
        {"name": "Standing Fan", "watts": 70},
        {"name": "LED Bulb", "watts": 10},
        {"name": "LCD TV", "watts": 100},
        {"name": "Fridge", "watts": 150},
        {"name": "Water Pump", "watts": 750},
        {"name": "Laptop", "watts": 65},
        {"name": "Phone Charger", "watts": 10},
        {"name": "Iron", "watts": 1000},
        {"name": "Electric Kettle", "watts": 1500},
        {"name": "Microwave", "watts": 1200}
    ]

    with app.app_context():
        # Check if we already have appliances
        if Appliance.query.first():
            print("Appliances already seeded.")
            return

        print("Seeding appliances...")
        for item in appliances_data:
            appliance = Appliance(name=item['name'], watts=item['watts'])
            db.session.add(appliance)
        
        db.session.commit()
        print("Seeding complete!")

if __name__ == '__main__':
    seed_appliances()
