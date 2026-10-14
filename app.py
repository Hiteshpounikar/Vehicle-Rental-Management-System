from datetime import date
import sqlite3
from pathlib import Path
from flask import Flask, abort, flash, redirect, render_template, request, url_for

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "vehicle_rental.db"
SCHEMA_PATH = ROOT / "database.sql"
app = Flask(__name__)
app.config["SECRET_KEY"] = "classroom-demo-change-before-deployment"

def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("PRAGMA foreign_keys=ON")
        db.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

def connect_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db

@app.template_filter("money")
def money(amount):
    return f"₹{float(amount):,.2f}"

@app.route("/")
def index():
    category = request.args.get("category", "")
    with connect_db() as db:
        if category in ("Car", "Bike", "SUV", "Van"):
            rows = db.execute("SELECT * FROM vehicles WHERE status='Available' AND category=? ORDER BY daily_rate", (category,)).fetchall()
        else:
            rows = db.execute("SELECT * FROM vehicles WHERE status='Available' ORDER BY category,daily_rate").fetchall()
    return render_template("index.html", vehicles=rows, selected_category=category)

@app.route("/book/<int:vehicle_id>", methods=["GET", "POST"])
def book(vehicle_id):
    with connect_db() as db:
        vehicle = db.execute("SELECT * FROM vehicles WHERE vehicle_id=? AND status='Available'", (vehicle_id,)).fetchone()
    if vehicle is None:
        abort(404)
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        license_no = request.form.get("driving_license_no", "").strip().upper()
        start_s = request.form.get("start_date", "")
        end_s = request.form.get("end_date", "")
        if not all((name, email, phone, license_no, start_s, end_s)):
            flash("Please complete every field.", "error")
        else:
            try:
                start = date.fromisoformat(start_s)
                end = date.fromisoformat(end_s)
            except ValueError:
                flash("Please enter valid dates.", "error")
            else:
                if start < date.today():
                    flash("Pickup date cannot be in the past.", "error")
                elif end < start:
                    flash("Return date must be on or after pickup date.", "error")
                else:
                    days = (end - start).days + 1
                    with connect_db() as db:
                        overlap = db.execute("""SELECT booking_id FROM bookings WHERE vehicle_id=?
                            AND booking_status='Confirmed' AND NOT (end_date < ? OR start_date > ?) LIMIT 1""",
                            (vehicle_id, start_s, end_s)).fetchone()
                        if overlap:
                            flash("Vehicle already has a booking during those dates.", "error")
                        else:
                            try:
                                db.execute("""INSERT INTO customers(full_name,email,phone,driving_license_no)
                                    VALUES(?,?,?,?) ON CONFLICT(email) DO UPDATE SET
                                    full_name=excluded.full_name, phone=excluded.phone,
                                    driving_license_no=excluded.driving_license_no""",
                                    (name, email, phone, license_no))
                                customer = db.execute("SELECT customer_id FROM customers WHERE email=?", (email,)).fetchone()
                                total = days * float(vehicle["daily_rate"])
                                cur = db.execute("""INSERT INTO bookings(customer_id,vehicle_id,start_date,end_date,total_days,total_amount)
                                    VALUES(?,?,?,?,?,?)""", (customer["customer_id"], vehicle_id, start_s, end_s, days, total))
                                booking_id = cur.lastrowid
                                db.execute("INSERT INTO payments(booking_id,amount) VALUES(?,?)", (booking_id, total))
                                db.commit()
                                return redirect(url_for("confirmation", booking_id=booking_id))
                            except sqlite3.IntegrityError:
                                db.rollback()
                                flash("Please verify the customer details; the licence number may already be registered.", "error")
    return render_template("book.html", vehicle=vehicle, today=date.today().isoformat())

@app.route("/confirmation/<int:booking_id>")
def confirmation(booking_id):
    with connect_db() as db:
        row = db.execute("""SELECT b.*,c.full_name,v.make,v.model,v.registration_no,p.payment_status
            FROM bookings b JOIN customers c ON c.customer_id=b.customer_id
            JOIN vehicles v ON v.vehicle_id=b.vehicle_id LEFT JOIN payments p ON p.booking_id=b.booking_id
            WHERE b.booking_id=?""", (booking_id,)).fetchone()
    if row is None:
        abort(404)
    return render_template("confirmation.html", booking=row)

@app.route("/admin")
def admin():
    with connect_db() as db:
        vehicles = db.execute("SELECT * FROM vehicles ORDER BY category,model").fetchall()
        bookings = db.execute("""SELECT b.*,c.full_name,v.make,v.model FROM bookings b
            JOIN customers c ON c.customer_id=b.customer_id JOIN vehicles v ON v.vehicle_id=b.vehicle_id
            ORDER BY b.created_at DESC""").fetchall()
        stats = {"vehicles": db.execute("SELECT COUNT(*) FROM vehicles").fetchone()[0],
                 "bookings": db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0],
                 "revenue": db.execute("SELECT COALESCE(SUM(total_amount),0) FROM bookings WHERE booking_status!='Cancelled'").fetchone()[0]}
    return render_template("admin.html", vehicles=vehicles, bookings=bookings, stats=stats)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
