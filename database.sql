PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS customers (
 customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
 full_name TEXT NOT NULL,
 email TEXT NOT NULL UNIQUE,
 phone TEXT NOT NULL,
 driving_license_no TEXT NOT NULL UNIQUE,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS vehicles (
 vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
 registration_no TEXT NOT NULL UNIQUE,
 make TEXT NOT NULL,
 model TEXT NOT NULL,
 category TEXT NOT NULL CHECK(category IN ('Car','Bike','SUV','Van')),
 seats INTEGER NOT NULL CHECK(seats > 0),
 fuel_type TEXT NOT NULL DEFAULT 'Petrol',
 daily_rate REAL NOT NULL CHECK(daily_rate >= 0),
 status TEXT NOT NULL DEFAULT 'Available' CHECK(status IN ('Available','Maintenance','Inactive'))
);
CREATE TABLE IF NOT EXISTS bookings (
 booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
 customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
 vehicle_id INTEGER NOT NULL REFERENCES vehicles(vehicle_id),
 start_date TEXT NOT NULL,
 end_date TEXT NOT NULL,
 total_days INTEGER NOT NULL CHECK(total_days > 0),
 total_amount REAL NOT NULL CHECK(total_amount >= 0),
 booking_status TEXT NOT NULL DEFAULT 'Confirmed' CHECK(booking_status IN ('Confirmed','Cancelled','Completed')),
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 CHECK(end_date >= start_date)
);
CREATE TABLE IF NOT EXISTS payments (
 payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
 booking_id INTEGER NOT NULL UNIQUE REFERENCES bookings(booking_id),
 amount REAL NOT NULL CHECK(amount >= 0),
 payment_method TEXT NOT NULL DEFAULT 'Pay at pickup',
 payment_status TEXT NOT NULL DEFAULT 'Pending' CHECK(payment_status IN ('Pending','Paid','Refunded')),
 paid_at TEXT
);
CREATE TABLE IF NOT EXISTS maintenance_records (
 maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
 vehicle_id INTEGER NOT NULL REFERENCES vehicles(vehicle_id),
 service_date TEXT NOT NULL,
 description TEXT NOT NULL,
 cost REAL NOT NULL DEFAULT 0 CHECK(cost >= 0)
);
CREATE INDEX IF NOT EXISTS idx_bookings_vehicle_dates ON bookings(vehicle_id,start_date,end_date,booking_status);
CREATE INDEX IF NOT EXISTS idx_bookings_customer ON bookings(customer_id);
INSERT OR IGNORE INTO vehicles(registration_no,make,model,category,seats,fuel_type,daily_rate,status) VALUES
('MH31AB1001','Maruti Suzuki','Swift','Car',5,'Petrol',1800,'Available'),
('MH31AB1002','Hyundai','i20','Car',5,'Petrol',2000,'Available'),
('MH31AB1003','Mahindra','Scorpio','SUV',7,'Diesel',3500,'Available'),
('MH31AB1004','Honda','Activa','Bike',2,'Petrol',500,'Available'),
('MH31AB1005','Royal Enfield','Classic 350','Bike',2,'Petrol',900,'Available'),
('MH31AB1006','Force','Traveller','Van',12,'Diesel',4500,'Available');
