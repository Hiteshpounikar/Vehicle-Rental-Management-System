# ER Diagram — Vehicle Rental Management System

```mermaid
erDiagram
    CUSTOMERS ||--o{ BOOKINGS : places
    VEHICLES ||--o{ BOOKINGS : assigned_to
    BOOKINGS ||--o| PAYMENTS : has
    VEHICLES ||--o{ MAINTENANCE_RECORDS : receives
    CUSTOMERS {
        int customer_id PK
        string full_name
        string email UK
        string phone
        string driving_license_no UK
    }
    VEHICLES {
        int vehicle_id PK
        string registration_no UK
        string make
        string model
        string category
        int seats
        string fuel_type
        decimal daily_rate
        string status
    }
    BOOKINGS {
        int booking_id PK
        int customer_id FK
        int vehicle_id FK
        date start_date
        date end_date
        int total_days
        decimal total_amount
        string booking_status
    }
    PAYMENTS {
        int payment_id PK
        int booking_id FK
        decimal amount
        string payment_status
    }
    MAINTENANCE_RECORDS {
        int maintenance_id PK
        int vehicle_id FK
        date service_date
        string description
        decimal cost
    }
```

A customer can make multiple bookings; a vehicle can be booked many times over time. Each booking can have one payment record, and a vehicle can have multiple maintenance records.
