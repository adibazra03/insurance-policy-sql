import oracledb as cx_Oracle

def get_connection():
    return cx_Oracle.connect(
        user="hpa5220",
        password="Pisco2003#",
        dsn="h3oracle.ad.psu.edu:1521/orclpdb.ad.psu.edu"
    )

# ---------------------------------------------------------------------------
# Display all customers
# ---------------------------------------------------------------------------

def display_customers():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT customer_id, first_name, last_name, email, phone,
                   date_of_birth, street, city, state, postal_code, created_at
            FROM customers
            ORDER BY customer_id
        """)

        rows = cursor.fetchall()

        print("\n" + "=" * 50)
        print("  CUSTOMERS")
        print("=" * 50)

        if not rows:
            print("  No customers found.")
        else:
            for row in rows:
                print(f"  ID           : {row[0]}")
                print(f"  Name         : {row[1]} {row[2]}")
                print(f"  Email        : {row[3]}")
                print(f"  Phone        : {row[4]}")
                print(f"  Date of Birth: {str(row[5]).split(' ')[0]}")
                print(f"  Address      : {row[6]}, {row[7]}, {row[8]} {row[9]}")
                print(f"  Created At   : {row[10]}")
                print("  " + "-" * 48)

        print(f"  Total: {len(rows)} customer(s)")
        print("=" * 50)

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ---------------------------------------------------------------------------
# Display all insurance policies
# ---------------------------------------------------------------------------

def display_policies():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT policy_id, customer_id, policy_number, policy_type,
                   coverage_amount, monthly_payment, start_date, end_date,
                   status, created_at
            FROM insurance_policies
            ORDER BY policy_id
        """)

        rows = cursor.fetchall()

        print("\n" + "=" * 76)
        print(f"  {'ID':<6} {'Cust ID':<8} {'Policy No.':<12} {'Type':<6} {'Coverage':>12} {'Monthly':>10} {'Start':<12} {'End':<12} {'Status'}")
        print("  " + "-" * 74)

        if not rows:
            print("  No policies found.")
        else:
            for row in rows:
                end = str(row[7]).split(' ')[0] if row[7] else "N/A"
                print(f"  {row[0]:<6} {row[1]:<8} {row[2]:<12} {row[3]:<6} {row[4]:>12,.2f} {row[5]:>10,.2f} {str(row[6]).split(' ')[0]:<12} {end:<12} {row[8]}")

        print("  " + "-" * 74)
        print(f"  Total: {len(rows)} policy(s)")
        print("=" * 76)

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ---------------------------------------------------------------------------
# Display all home policy details
# ---------------------------------------------------------------------------

def display_home_policies():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT policy_id, house_address, house_area, bedrooms, bathrooms, house_price
            FROM home_policy_details
            ORDER BY policy_id
        """)

        rows = cursor.fetchall()

        print("\n" + "=" * 50)
        print("  HOME POLICY DETAILS")
        print("=" * 50)

        if not rows:
            print("  No home policies found.")
        else:
            for row in rows:
                print(f"  Policy ID    : {row[0]}")
                print(f"  Address      : {row[1]}")
                print(f"  Area         : {row[2]:,.2f} sq ft")
                print(f"  Bedrooms     : {row[3]}")
                print(f"  Bathrooms    : {row[4]}")
                print(f"  House Price  : ${row[5]:,.2f}")
                print("  " + "-" * 48)

        print(f"  Total: {len(rows)} home policy(s)")
        print("=" * 50)

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ---------------------------------------------------------------------------
# Display all car policy details
# ---------------------------------------------------------------------------

def display_car_policies():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT policy_id, make, model, car_year, vin, mileage_per_year
            FROM car_policy_details
            ORDER BY policy_id
        """)

        rows = cursor.fetchall()

        print("\n" + "=" * 70)
        print(f"  {'ID':<6} {'Make':<12} {'Model':<12} {'Year':<6} {'VIN':<20} {'Mileage/Yr':>10}")
        print("  " + "-" * 68)

        if not rows:
            print("  No car policies found.")
        else:
            for row in rows:
                print(f"  {row[0]:<6} {row[1]:<12} {row[2]:<12} {row[3]:<6} {row[4]:<20} {row[5]:>10,}")

        print("  " + "-" * 68)
        print(f"  Total: {len(rows)} car policy(s)")
        print("=" * 70)

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# ---------------------------------------------------------------------------
# Display all life policy details
# ---------------------------------------------------------------------------

def display_life_policies():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT policy_id, existing_conditions, beneficiary
            FROM life_policy_details
            ORDER BY policy_id
        """)

        rows = cursor.fetchall()

        print("\n" + "=" * 50)
        print("  LIFE POLICY DETAILS")
        print("=" * 50)

        if not rows:
            print("  No life policies found.")
        else:
            for row in rows:
                print(f"  Policy ID    : {row[0]}")
                print(f"  Conditions   : {row[1] if row[1] else 'None'}")
                print(f"  Beneficiary  : {row[2]}")
                print("  " + "-" * 48)

        print(f"  Total: {len(rows)} life policy(s)")
        print("=" * 50)

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
