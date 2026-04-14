import oracledb as cx_Oracle

# ---------------------------------------------------------------------------
# Database connection
# ---------------------------------------------------------------------------

def get_connection():
    return cx_Oracle.connect(
        user="hpa5220",
        password="Pisco2003#",
        dsn="h3oracle.ad.psu.edu:1521/orclpdb.ad.psu.edu"
    )

# ---------------------------------------------------------------------------
# Add customer + insurance policy
# ---------------------------------------------------------------------------

def add_customer():
    print("\n--- Add New Customer ---")

    # Collect customer details
    first_name   = input("First name: ").strip()
    last_name    = input("Last name: ").strip()
    email        = input("Email: ").strip()
    phone        = input("Phone: ").strip()
    dob          = input("Date of birth (YYYY-MM-DD): ").strip()
    street       = input("Street: ").strip()
    city         = input("City: ").strip()
    state        = input("State: ").strip()
    postal_code  = input("Postal code: ").strip()

    # Choose policy type
    print("\nPolicy types: HOME, CAR, LIFE")
    policy_type = input("Policy type: ").strip().upper()
    while policy_type not in ("HOME", "CAR", "LIFE"):
        print("Invalid type. Choose HOME, CAR, or LIFE.")
        policy_type = input("Policy type: ").strip().upper()

    # Collect shared policy details
    policy_number   = input("Policy number (e.g. HOME-1002): ").strip()
    coverage_amount = input("Coverage amount: ").strip()
    monthly_payment = input("Monthly payment: ").strip()
    start_date      = input("Start date (YYYY-MM-DD): ").strip()
    end_date        = input("End date (YYYY-MM-DD, or leave blank for none): ").strip()
    end_date        = end_date if end_date else None

    # Collect policy-type-specific details
    policy_details = {}
    if policy_type == "HOME":
        policy_details["house_address"] = input("House address: ").strip()
        policy_details["house_area"]    = input("House area (sq ft): ").strip()
        policy_details["bedrooms"]      = input("Number of bedrooms: ").strip()
        policy_details["bathrooms"]     = input("Number of bathrooms: ").strip()
        policy_details["house_price"]   = input("House price: ").strip()

    elif policy_type == "CAR":
        policy_details["make"]             = input("Car make: ").strip()
        policy_details["model"]            = input("Car model: ").strip()
        policy_details["car_year"]         = input("Car year: ").strip()
        policy_details["vin"]              = input("VIN: ").strip()
        policy_details["mileage_per_year"] = input("Mileage per year: ").strip()

    elif policy_type == "LIFE":
        policy_details["existing_conditions"] = input("Existing conditions (or leave blank): ").strip() or None
        policy_details["beneficiary"]         = input("Beneficiary name: ").strip()

    # --- Write to database ---
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # 1. Insert customer
        cursor.execute("""
            INSERT INTO customers (
                first_name, last_name, email, phone, date_of_birth,
                street, city, state, postal_code
            ) VALUES (
                :first_name, :last_name, :email, :phone,
                TO_DATE(:dob, 'YYYY-MM-DD'),
                :street, :city, :state, :postal_code
            )
        """, {
            "first_name": first_name, "last_name": last_name,
            "email": email, "phone": phone, "dob": dob,
            "street": street, "city": city, "state": state,
            "postal_code": postal_code
        })

        # Retrieve the generated customer_id
        cursor.execute("SELECT MAX(customer_id) FROM customers")
        customer_id = cursor.fetchone()[0]

        # 2. Insert insurance policy
        cursor.execute("""
            INSERT INTO insurance_policies (
                customer_id, policy_number, policy_type, coverage_amount,
                monthly_payment, start_date, end_date, status
            ) VALUES (
                :customer_id, :policy_number, :policy_type, :coverage_amount,
                :monthly_payment,
                TO_DATE(:start_date, 'YYYY-MM-DD'),
                TO_DATE(:end_date, 'YYYY-MM-DD'),
                'ACTIVE'
            )
        """, {
            "customer_id": customer_id, "policy_number": policy_number,
            "policy_type": policy_type, "coverage_amount": coverage_amount,
            "monthly_payment": monthly_payment, "start_date": start_date,
            "end_date": end_date
        })

        # Retrieve the generated policy_id
        cursor.execute("SELECT MAX(policy_id) FROM insurance_policies")
        policy_id = cursor.fetchone()[0]

        # 3. Insert policy-type-specific details
        if policy_type == "HOME":
            cursor.execute("""
                INSERT INTO home_policy_details (
                    policy_id, house_address, house_area, bedrooms, bathrooms, house_price
                ) VALUES (
                    :policy_id, :house_address, :house_area, :bedrooms, :bathrooms, :house_price
                )
            """, {"policy_id": policy_id, **policy_details})

        elif policy_type == "CAR":
            cursor.execute("""
                INSERT INTO car_policy_details (
                    policy_id, make, model, car_year, vin, mileage_per_year
                ) VALUES (
                    :policy_id, :make, :model, :car_year, :vin, :mileage_per_year
                )
            """, {"policy_id": policy_id, **policy_details})

        elif policy_type == "LIFE":
            cursor.execute("""
                INSERT INTO life_policy_details (
                    policy_id, existing_conditions, beneficiary
                ) VALUES (
                    :policy_id, :existing_conditions, :beneficiary
                )
            """, {"policy_id": policy_id, **policy_details})

        connection.commit()
        print(f"\nCustomer '{first_name} {last_name}' added with {policy_type} policy (ID: {policy_id}).")

    except cx_Oracle.DatabaseError as e:
        if connection:
            connection.rollback()
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# ---------------------------------------------------------------------------
# Add policy to existing customer
# ---------------------------------------------------------------------------

def add_policy():
    print("\n--- Add Policy to Existing Customer ---")

    first_name = input("Customer first name: ").strip()
    last_name  = input("Customer last name: ").strip()

    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Look up customer by name
        cursor.execute("""
            SELECT customer_id, first_name, last_name
            FROM customers
            WHERE LOWER(first_name) = LOWER(:first) AND LOWER(last_name) = LOWER(:last)
        """, {"first": first_name, "last": last_name})

        rows = cursor.fetchall()

        if not rows:
            print(f"No customer found with name '{first_name} {last_name}'.")
            return

        # Handle multiple matches (e.g. two people with the same name)
        if len(rows) > 1:
            print("Multiple customers found:")
            for row in rows:
                print(f"  ID: {row[0]} — {row[1]} {row[2]}")
            customer_id = input("Enter the customer ID to use: ").strip()
        else:
            customer_id = rows[0][0]
            print(f"Customer found — ID: {customer_id}, Name: {rows[0][1]} {rows[0][2]}")

        # Choose policy type
        print("\nPolicy types: HOME, CAR, LIFE")
        policy_type = input("Policy type: ").strip().upper()
        while policy_type not in ("HOME", "CAR", "LIFE"):
            print("Invalid type. Choose HOME, CAR, or LIFE.")
            policy_type = input("Policy type: ").strip().upper()

        # Shared policy details
        policy_number   = input("Policy number (e.g. CAR-1005): ").strip()
        coverage_amount = input("Coverage amount: ").strip()
        monthly_payment = input("Monthly payment: ").strip()
        start_date      = input("Start date (YYYY-MM-DD): ").strip()
        end_date        = input("End date (YYYY-MM-DD, or leave blank for none): ").strip()
        end_date        = end_date if end_date else None

        # Policy-type-specific details
        policy_details = {}
        if policy_type == "HOME":
            policy_details["house_address"] = input("House address: ").strip()
            policy_details["house_area"]    = input("House area (sq ft): ").strip()
            policy_details["bedrooms"]      = input("Number of bedrooms: ").strip()
            policy_details["bathrooms"]     = input("Number of bathrooms: ").strip()
            policy_details["house_price"]   = input("House price: ").strip()

        elif policy_type == "CAR":
            policy_details["make"]             = input("Car make: ").strip()
            policy_details["model"]            = input("Car model: ").strip()
            policy_details["car_year"]         = input("Car year: ").strip()
            policy_details["vin"]              = input("VIN: ").strip()
            policy_details["mileage_per_year"] = input("Mileage per year: ").strip()

        elif policy_type == "LIFE":
            policy_details["existing_conditions"] = input("Existing conditions (or leave blank): ").strip() or None
            policy_details["beneficiary"]         = input("Beneficiary name: ").strip()

        # 1. Insert policy
        cursor.execute("""
            INSERT INTO insurance_policies (
                customer_id, policy_number, policy_type, coverage_amount,
                monthly_payment, start_date, end_date, status
            ) VALUES (
                :customer_id, :policy_number, :policy_type, :coverage_amount,
                :monthly_payment,
                TO_DATE(:start_date, 'YYYY-MM-DD'),
                TO_DATE(:end_date, 'YYYY-MM-DD'),
                'ACTIVE'
            )
        """, {
            "customer_id": customer_id, "policy_number": policy_number,
            "policy_type": policy_type, "coverage_amount": coverage_amount,
            "monthly_payment": monthly_payment, "start_date": start_date,
            "end_date": end_date
        })

        # Retrieve the generated policy_id
        cursor.execute("SELECT MAX(policy_id) FROM insurance_policies")
        policy_id = cursor.fetchone()[0]

        # 2. Insert policy-type-specific details
        if policy_type == "HOME":
            cursor.execute("""
                INSERT INTO home_policy_details (
                    policy_id, house_address, house_area, bedrooms, bathrooms, house_price
                ) VALUES (
                    :policy_id, :house_address, :house_area, :bedrooms, :bathrooms, :house_price
                )
            """, {"policy_id": policy_id, **policy_details})

        elif policy_type == "CAR":
            cursor.execute("""
                INSERT INTO car_policy_details (
                    policy_id, make, model, car_year, vin, mileage_per_year
                ) VALUES (
                    :policy_id, :make, :model, :car_year, :vin, :mileage_per_year
                )
            """, {"policy_id": policy_id, **policy_details})

        elif policy_type == "LIFE":
            cursor.execute("""
                INSERT INTO life_policy_details (
                    policy_id, existing_conditions, beneficiary
                ) VALUES (
                    :policy_id, :existing_conditions, :beneficiary
                )
            """, {"policy_id": policy_id, **policy_details})

        connection.commit()
        print(f"\n{policy_type} policy (ID: {policy_id}) added for customer ID {customer_id}.")

    except cx_Oracle.DatabaseError as e:
        if connection:
            connection.rollback()
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
