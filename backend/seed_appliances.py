from app import app, db, Appliance

def seed_appliances():
    appliances = [
        {'name': '1HP Inverter AC', 'default_watts': 900},
        {'name': 'Standing Fan', 'default_watts': 50},
        {'name': 'Deep Freezer (Medium)', 'default_watts': 200},
        {'name': 'LED Bulb', 'default_watts': 10},
        {'name': 'Laptop', 'default_watts': 65},
        {'name': 'TV (43 inch LED)', 'default_watts': 80},
        {'name': 'Phone Charger', 'default_watts': 15},
        {'name': 'Refrigerator (Medium)', 'default_watts': 150},
        {'name': 'Water Pumping Machine (0.5HP)', 'default_watts': 375},
        {'name': 'Microwave', 'default_watts': 1000}
    ]

    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if already seeded to avoid duplicates
        if Appliance.query.first():
            print("Appliances table already has data. Skipping seed.")
            return

        for item in appliances:
            appliance = Appliance(name=item['name'], default_watts=item['default_watts'])
            db.session.add(appliance)
        
        db.session.commit()
        print("Appliances seeded successfully.")

if __name__ == '__main__':
    seed_appliances()
