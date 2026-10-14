# Vehicle Rental Management System

DBMS mini-project using Python, Flask, SQLite, HTML and CSS.

## Features
- Browse vehicles and filter by category
- Book vehicles for selected dates
- Validate booking dates and detect overlapping bookings
- Calculate rental amount
- Booking confirmation and admin dashboard
- SQLite schema with customers, vehicles, bookings, payments and maintenance records

## Run locally
1. Install Python 3.10+
2. Download/clone this repository.
3. Run `python -m venv .venv`
4. Windows: `.venv\Scripts\activate`
5. Run `pip install -r requirements.txt`
6. Run `python app.py`
7. Open http://127.0.0.1:5000

The database is initialized from `database.sql` on first run. This is a classroom demo: the admin page has no login protection and should not be deployed publicly as-is. Use sample details only and add real screenshots from your own run before submitting your report.

## Contents
- `app.py` — Flask source code
- `database.sql` — database schema and sample vehicle data
- `templates/` — HTML templates
- `static/style.css` — styles
- `docs/PROJECT_REPORT.md` — report text
- `docs/ER_DIAGRAM.md` — ER diagram
