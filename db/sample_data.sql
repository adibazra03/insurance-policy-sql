INSERT INTO customers (
    first_name, last_name, email, phone, date_of_birth, street, city, state, postal_code
) VALUES (
    'John', 'Carter', 'john.carter@example.com', '814-555-1001',
    DATE '1987-02-11', '12 Oak Street', 'State College', 'PA', '16801'
);

INSERT INTO customers (
    first_name, last_name, email, phone, date_of_birth, street, city, state, postal_code
) VALUES (
    'Maria', 'Lopez', 'maria.lopez@example.com', '717-555-2030',
    DATE '1992-06-19', '89 Pine Avenue', 'Harrisburg', 'PA', '17101'
);

INSERT INTO customers (
    first_name, last_name, email, phone, date_of_birth, street, city, state, postal_code
) VALUES (
    'Amir', 'Patel', 'amir.patel@example.com', '610-555-8812',
    DATE '1979-10-03', '455 Cedar Lane', 'Allentown', 'PA', '18101'
);

INSERT INTO insurance_policies (
    customer_id, policy_number, policy_type, coverage_amount, monthly_payment,
    start_date, end_date, status
) VALUES (
    1, 'HOME-1001', 'HOME', 350000, 165.50,
    DATE '2026-01-01', DATE '2026-12-31', 'ACTIVE'
);

INSERT INTO home_policy_details (
    policy_id, house_address, house_area, bedrooms, bathrooms, house_price
) VALUES (
    1, '12 Oak Street, State College, PA 16801', 2100, 4, 3, 415000
);

INSERT INTO insurance_policies (
    customer_id, policy_number, policy_type, coverage_amount, monthly_payment,
    start_date, end_date, status
) VALUES (
    2, 'CAR-2001', 'CAR', 50000, 118.75,
    DATE '2026-02-15', DATE '2027-02-14', 'ACTIVE'
);

INSERT INTO car_policy_details (
    policy_id, make, model, car_year, vin, mileage_per_year
) VALUES (
    2, 'Toyota', 'Camry', 2022, '1HGBH41JXMN109186', 12000
);

INSERT INTO insurance_policies (
    customer_id, policy_number, policy_type, coverage_amount, monthly_payment,
    start_date, end_date, status
) VALUES (
    3, 'LIFE-3001', 'LIFE', 250000, 92.00,
    DATE '2026-03-01', NULL, 'ACTIVE'
);

INSERT INTO life_policy_details (
    policy_id, existing_conditions, beneficiary
) VALUES (
    3, 'Mild asthma', 'Aisha Patel'
);

COMMIT;

