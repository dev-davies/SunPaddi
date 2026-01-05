from app import app
from models import db, Product

def add_test():
    with app.app_context():
        # Add normal product
        p1 = Product(name="Normal Panel", category="solar_panel", price=50000, stock=10, is_sponsored=False)
        # Add sponsored product
        p2 = Product(name="Sponsored Panel", category="solar_panel", price=60000, stock=10, is_sponsored=True)
        
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        print("Added products")

if __name__ == '__main__':
    add_test()
