# SunPaddi Partner Guide

## How to Add Partner Vendors (Sponsored Products)

To add products from partner vendors that should appear at the top of search results (Sponsored), follow these steps:

### 1. Database Access

You can access the SQLite database directly or use a Python script.

### 2. Adding a Sponsored Product via Python Script

Create a script (e.g., `add_partner_product.py`) in the `backend/` directory:

```python
from app import app
from models import db, Product

def add_sponsored_product():
    with app.app_context():
        new_product = Product(
            name="Premium Solar Panel 600W",
            category="solar_panel",
            specs={"brand": "SunPartner", "warranty": "25 years"},
            price=150000.0,
            stock=50,
            is_sponsored=True  # This flags it as sponsored
        )
        db.session.add(new_product)
        db.session.commit()
        print("Sponsored product added successfully!")

if __name__ == '__main__':
    add_sponsored_product()
```

### 3. Adding via SQL

If you are using a SQLite viewer or client:

```sql
INSERT INTO product (name, category, specs, price, stock, is_sponsored)
VALUES ('Partner Battery 200Ah', 'battery', '{}', 250000, 10, 1);
```

### 4. Verification

Call the products API to see sponsored items first:
`GET http://localhost:5000/api/products`
