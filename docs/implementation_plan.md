# SunPaddi Backend Setup Plan

## Goal Description
Set up a Python Flask backend for the SunPaddi solar energy app. The backend will serve as the API for a mobile frontend.

## Proposed Changes

### Setup
#### [NEW] [requirements.txt](file:///C:/Users/Novel/.gemini/antigravity/scratch/SunPaddi/backend/requirements.txt)
- Add `Flask`, `Flask-CORS`, `Flask-SQLAlchemy`, `beautifulsoup4`.

#### [NEW] [app.py](file:///C:/Users/Novel/.gemini/antigravity/scratch/SunPaddi/backend/app.py)
- Initialize Flask app.
- Configure CORS.
- Set up a basic root route returning "SunPaddi API is live".

## Verification Plan

### Automated Tests
- Run `python app.py` and check for successful startup.
- Use `curl` or browser to hit `http://localhost:5000/` and verify response.

# Database Integration Plan

## Goal Description
Integrate SQLite database using SQLAlchemy. Define models for Products, Appliances, and Leads. Seed Appliances with common Nigerian electronics.

## Proposed Changes

### Backend
#### [MODIFY] [app.py](file:///C:/Users/Novel/.gemini/antigravity/scratch/SunPaddi/backend/app.py)
- Configure `Flask-SQLAlchemy` with SQLite `sunpaddi.db`.
- Define models:
    - `Product`: id, brand, type, specs, price, vendor_url, last_updated.
    - `Appliance`: id, name, default_watts.
    - `Lead`: id, user_phone, system_recommended, timestamp.

#### [NEW] [seed_appliances.py](file:///C:/Users/Novel/.gemini/antigravity/scratch/SunPaddi/backend/seed_appliances.py)
- Script to initialize the database and insert default appliances (1HP AC, Standing Fan, Deep Freezer, LED Bulb, etc.).

## Verification Plan

### Automated Tests
- Run `python seed_appliances.py` to create DB and populate data.
- Run a verification script or `flask shell` to query `Appliance.query.all()` and print results.

