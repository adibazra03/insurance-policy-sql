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
# Remove customer
# ---------------------------------------------------------------------------

def remove_customer():
    print("\n--- Remove Customer ---")

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

        # Handle multiple matches
        if len(rows) > 1:
            print("Multiple customers found:")
            for row in rows:
                print(f"  ID: {row[0]} — {row[1]} {row[2]}")
            customer_id = input("Enter the customer ID to remove: ").strip()
        else:
            customer_id = rows[0][0]
            print(f"Customer found — ID: {customer_id}, Name: {rows[0][1]} {rows[0][2]}")

        # Confirm before deleting
        confirm = input(f"Are you sure you want to remove this customer and all their policies? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return

        # Delete customer — CASCADE will automatically remove their policies and policy details
        cursor.execute("""
            DELETE FROM customers WHERE customer_id = :customer_id
        """, {"customer_id": customer_id})

        connection.commit()
        print(f"Customer ID {customer_id} and all associated policies removed.")

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
# Remove policy
# ---------------------------------------------------------------------------

def remove_policy():
    print("\n--- Remove Policy ---")

    first_name = input("Customer first name: ").strip()
    last_name  = input("Customer last name: ").strip()
    email      = input("Customer email: ").strip()

    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Look up customer by first name, last name, and email
        cursor.execute("""
            SELECT customer_id, first_name, last_name, email
            FROM customers
            WHERE LOWER(first_name) = LOWER(:first)
              AND LOWER(last_name)  = LOWER(:last)
              AND LOWER(email)      = LOWER(:email)
        """, {"first": first_name, "last": last_name, "email": email})

        row = cursor.fetchone()

        if not row:
            print(f"No customer found with that name and email.")
            return

        customer_id = row[0]
        print(f"\nCustomer found — ID: {customer_id}, Name: {row[1]} {row[2]}, Email: {row[3]}")

        # Display all policies belonging to this customer
        cursor.execute("""
            SELECT policy_id, policy_number, policy_type, coverage_amount,
                   monthly_payment, start_date, end_date, status
            FROM insurance_policies
            WHERE customer_id = :customer_id
            ORDER BY policy_id
        """, {"customer_id": customer_id})

        policies = cursor.fetchall()

        if not policies:
            print("This customer has no policies.")
            return

        print("\nPolicies:")
        print(f"  {'ID':<6} {'Policy No.':<12} {'Type':<6} {'Coverage':>12} {'Monthly':>10} {'Start':<12} {'End':<12} {'Status'}")
        print("  " + "-" * 80)
        for p in policies:
            end = str(p[6].date()) if p[6] else "N/A"
            print(f"  {p[0]:<6} {p[1]:<12} {p[2]:<6} {p[3]:>12,.2f} {p[4]:>10,.2f} {str(p[5].date()):<12} {end:<12} {p[7]}")

        # Ask which policy to remove
        policy_id = input("\nEnter the policy ID to remove: ").strip()

        # Verify the policy belongs to this customer
        cursor.execute("""
            SELECT policy_id FROM insurance_policies
            WHERE policy_id = :policy_id AND customer_id = :customer_id
        """, {"policy_id": policy_id, "customer_id": customer_id})

        if not cursor.fetchone():
            print("Policy not found for this customer.")
            return

        # Confirm before deleting
        confirm = input(f"Are you sure you want to remove policy ID {policy_id}? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return

        # Delete policy — CASCADE removes the detail row automatically
        cursor.execute("""
            DELETE FROM insurance_policies WHERE policy_id = :policy_id
        """, {"policy_id": policy_id})

        connection.commit()
        print(f"Policy ID {policy_id} removed.")

    except cx_Oracle.DatabaseError as e:
        if connection:
            connection.rollback()
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
