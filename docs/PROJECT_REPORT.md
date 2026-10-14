# Vehicle Rental Management System — DBMS Mini-Project Report

**Student:** Hitesh Lomesh Pounikar  
**Branch:** Information Technology  
**Year:** Third Year B.Tech  
**Institute:** Priyadarshini College of Engineering, Nagpur  
**Academic Year:** 2026–2027

> Confirm the details required by your department. Add actual screenshots captured from your running application before submission. This is editable report text, not a PDF.

## 1. Abstract
The Vehicle Rental Management System is a database-driven application that helps organize vehicle inventory, customer details, rental bookings, payment status, and maintenance records. It uses Python Flask for the web application and SQLite for persistent data storage.

## 2. Problem Statement
Manual rental records can result in duplicate entries, booking conflicts, incorrect rental calculations, and difficulty retrieving customer and vehicle information. This system centralizes records and applies validation and database constraints.

## 3. Objectives
- Store vehicle and customer details in a relational database.
- Browse vehicles by category and availability.
- Create bookings with pickup and return dates.
- Calculate rental costs automatically.
- Detect overlapping confirmed bookings.
- Demonstrate primary keys, foreign keys, constraints, joins, and indexes.

## 4. Scope
The prototype provides vehicle browsing, booking, confirmation, and a basic dashboard. It does not include secure admin login, a payment gateway, or live notifications.

## 5. Requirements
Hardware: computer with a modern browser. Software: Python 3.10+, Flask, SQLite, HTML5, CSS3, and an editor such as Visual Studio Code.

## 6. Modules
1. Vehicle management — registration, make, model, category, seats, fuel, rate, and status.
2. Customer management — name, email, phone, and driving licence number.
3. Booking management — dates, availability conflict checks, and booking status.
4. Rental calculation — daily rate multiplied by rental days.
5. Payment management — amount and payment status.
6. Maintenance records — service date, description, and cost.
7. Dashboard — vehicle inventory, bookings, and total booked value.

## 7. Database Design
The schema includes customers, vehicles, bookings, payments, and maintenance_records. Primary keys identify each record. Foreign keys connect bookings to customers and vehicles, payments to bookings, and maintenance records to vehicles. Unique and CHECK constraints improve data consistency. Indexes help common booking lookups. See `database.sql` and `ER_DIAGRAM.md`.

## 8. Workflow
1. User browses the vehicle catalogue and optionally filters by category.
2. User selects a vehicle and enters contact information and rental dates.
3. The application validates fields and dates.
4. The system checks for overlapping confirmed bookings.
5. A valid booking and pending payment record are stored.
6. The total is calculated and a confirmation page is shown.
7. The dashboard displays inventory and bookings.

## 9. Cost Formula
**Total rental amount = Daily rate × Number of rental days.** This demo counts both pickup and return dates as rental days.

## 10. Sample SQL Queries
Available vehicles:
```sql
SELECT * FROM vehicles WHERE status='Available' ORDER BY daily_rate;
```
Bookings with customer and vehicle:
```sql
SELECT b.booking_id,c.full_name,v.make,v.model,b.start_date,b.end_date,b.total_amount
FROM bookings b JOIN customers c ON c.customer_id=b.customer_id
JOIN vehicles v ON v.vehicle_id=b.vehicle_id;
```
Total value of non-cancelled bookings:
```sql
SELECT COALESCE(SUM(total_amount),0) AS total_booking_value
FROM bookings WHERE booking_status <> 'Cancelled';
```
Vehicle count by category:
```sql
SELECT category,COUNT(*) AS vehicle_count FROM vehicles GROUP BY category;
```

## 11. Testing Plan
Test the home page, category filters, valid booking, missing fields, past pickup date, return date before pickup, overlapping booking dates, confirmation details, and dashboard listing. Record the actual results and attach screenshots from your own application run.

## 12. Advantages
- Centralized rental data and faster searches.
- Reduced duplicate and inconsistent records.
- Automated cost calculation.
- Referential integrity through foreign keys.
- Simple setup using SQLite.

## 13. Limitations
The admin dashboard has no authentication. Payment processing is not integrated. The inventory is sample data. This is an academic prototype and requires security hardening before deployment.

## 14. Future Scope
Add role-based login, payment gateway integration, email/SMS notifications, cancellation and refund workflows, vehicle photos, reporting, database backups, and secure deployment.

## 15. Conclusion
The project demonstrates how a relational database can support vehicle rental operations. It combines customer, vehicle, booking, payment, and maintenance data with constraints and relationships. The Flask interface demonstrates browsing, booking validation, rental calculations, and booking confirmation.

## 16. References
- Python: https://docs.python.org/3/
- Flask: https://flask.palletsprojects.com/
- SQLite: https://www.sqlite.org/docs.html
