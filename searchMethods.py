import oracledb as cx_Oracle 
def get_connection():
    return cx_Oracle.connect(
        user="hpa5220",
        password="Pisco2003#",
        dsn="h3oracle.ad.psu.edu:1521/orclpdb.ad.psu.edu"
    )

#search for customer 
def search_customer():
    print("/n--- Searchg Customer---")
    first_name = input("first name: ").strip()
    last_name = input("last name: ").strip()
    email = input("email: ").strip()

    connection = None
    cursor =None

    try:
        connection = get_connection()
        cursor = connection.cursor()
        # select for customer that matches input
        cursor.execute("""
            SELECT customer_id, first_name,last_name, email,phone, date_of_birth, street, city,state, postal_code, created_at
            FROM customers
            WHERE first_name = :first_name AND last_name = :last_name AND email = :email
        """, {
            "first_name": first_name,
            "last_name": last_name,
            "email": email
        })

        rows = cursor.fetchall()
        if not rows:
            print(f"No customer found with name {first_name} {last_name} and email: {email}")
            return
        else:
            print("\nCustomer found:")
            print("-" * 40)
            for row in rows:
                print(f"  ID           : {row[0]}")
                print(f"  Name         : {row[1]} {row[2]}")
                print(f"  Email        : {row[3]}")
                print(f"  Phone        : {row[4]}")
                print(f"  Date of Birth: {str(row[5]).split(' ')[0]}")
                print(f"  Address      : {row[6]}, {row[7]}, {row[8]} {row[9]}")
                print(f"  Created At   : {row[10]}")
            print("-" * 40)
            
            #option to display active policies
            show_policies = input("Do you want to see active policies for this customer? (yes/no): ").strip().lower()
            if show_policies == "yes":
                cursor.execute("""
                    SELECT policy_id, policy_number, policy_type, coverage_amount, monthly_payment, start_date, end_date, status
                    FROM insurance_policies
                    WHERE customer_id = :customer_id AND status = 'ACTIVE'
                """, {"customer_id": rows[0][0]})

                policies = cursor.fetchall()
                if not policies:
                    print("No active policies found for this customer.")
                else:
                    print("\nActive Policies:")
                    print(f"  {'ID':<6} {'Policy No.':<12} {'Type':<6} {'Coverage':>12} {'Monthly':>10} {'Start':<12} {'End':<12} {'Status'}")
                    print("  " + "-" * 76)
                    for policy in policies:
                        end = str(policy[6]).split(' ')[0] if policy[6] else "N/A"
                        print(f"  {policy[0]:<6} {policy[1]:<12} {policy[2]:<6} {policy[3]:>12,.2f} {policy[4]:>10,.2f} {str(policy[5]).split(' ')[0]:<12} {end:<12} {policy[7]}")
                    counter =0
                    while (counter == 0):
                        decision = input("Would you like to see details of any policies listed above?: ").strip().lower()
                        if decision == "yes":
                            search_policy()
                        elif decision == "no":
                            print("Returning to main menu.")
                            counter += 1
                        else:
                            print("Invalid input, please enter yes or no")
                                  
            if show_policies == "no":
                print("Returning to main menu.")
                return
        
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
# Search policy by ID — displays full details based on policy type
# ---------------------------------------------------------------------------

def search_policy():
    print("\n--- Search Policy by ID ---")
    policy_id = input("Enter policy ID: ").strip()

    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Get base policy info and determine type
        cursor.execute("""
            SELECT p.policy_id, p.policy_number, p.policy_type, p.coverage_amount,
                   p.monthly_payment, p.start_date, p.end_date, p.status,
                   c.customer_id, c.first_name, c.last_name, c.email
            FROM insurance_policies p
            JOIN customers c ON c.customer_id = p.customer_id
            WHERE p.policy_id = :policy_id
        """, {"policy_id": policy_id})

        row = cursor.fetchone()

        if not row:
            print(f"No policy found with ID {policy_id}.")
            return

        policy_type = row[2]

        # Print base policy info
        print("\n" + "=" * 40)
        print(f"  Policy Details — {policy_type}")
        print("=" * 40)
        print(f"  Policy ID      : {row[0]}")
        print(f"  Policy Number  : {row[1]}")
        print(f"  Policy Type    : {row[2]}")
        print(f"  Coverage Amount: ${row[3]:,.2f}")
        print(f"  Monthly Payment: ${row[4]:,.2f}")
        print(f"  Start Date     : {str(row[5]).split(' ')[0]}")
        print(f"  End Date       : {str(row[6]).split(' ')[0] if row[6] else 'N/A'}")
        print(f"  Status         : {row[7]}")
        print(f"  Customer       : {row[9]} {row[10]} (ID: {row[8]})")
        print(f"  Email          : {row[11]}")
        print("-" * 40)

        # Fetch and print type-specific details
        if policy_type == "HOME":
            cursor.execute("""
                SELECT house_address, house_area, bedrooms, bathrooms, house_price
                FROM home_policy_details
                WHERE policy_id = :policy_id
            """, {"policy_id": policy_id})
            detail = cursor.fetchone()
            if detail:
                print(f"  House Address  : {detail[0]}")
                print(f"  House Area     : {detail[1]:,.2f} sq ft")
                print(f"  Bedrooms       : {detail[2]}")
                print(f"  Bathrooms      : {detail[3]}")
                print(f"  House Price    : ${detail[4]:,.2f}")

        elif policy_type == "CAR":
            cursor.execute("""
                SELECT make, model, car_year, vin, mileage_per_year
                FROM car_policy_details
                WHERE policy_id = :policy_id
            """, {"policy_id": policy_id})
            detail = cursor.fetchone()
            if detail:
                print(f"  Make           : {detail[0]}")
                print(f"  Model          : {detail[1]}")
                print(f"  Year           : {detail[2]}")
                print(f"  VIN            : {detail[3]}")
                print(f"  Mileage/Year   : {detail[4]:,}")

        elif policy_type == "LIFE":
            cursor.execute("""
                SELECT existing_conditions, beneficiary
                FROM life_policy_details
                WHERE policy_id = :policy_id
            """, {"policy_id": policy_id})
            detail = cursor.fetchone()
            if detail:
                print(f"  Conditions     : {detail[0] if detail[0] else 'None'}")
                print(f"  Beneficiary    : {detail[1]}")

        print("=" * 40)

    except cx_Oracle.DatabaseError as e:
        print(f"Database error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
