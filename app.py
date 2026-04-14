from flask import Flask, render_template, request, redirect, url_for, flash
import oracledb as cx_Oracle

app = Flask(__name__)
app.secret_key = "insurance_mgmt_secret"

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
# Home / Dashboard
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    stats = {}
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM customers")
        stats["customers"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM insurance_policies")
        stats["policies"] = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM insurance_policies WHERE status='ACTIVE'")
        stats["active"] = cur.fetchone()[0]
        cur.close()
        conn.close()
    except Exception as e:
        stats = {"customers": "—", "policies": "—", "active": "—"}
        flash(f"DB error: {e}", "danger")
    return render_template("index.html", stats=stats)

# ---------------------------------------------------------------------------
# Display — Customers
# ---------------------------------------------------------------------------

@app.route("/customers")
def customers_list():
    rows = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT customer_id, first_name, last_name, email, phone,
                   date_of_birth, street, city, state, postal_code, created_at
            FROM customers ORDER BY customer_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"DB error: {e}", "danger")
    return render_template("customers_list.html", rows=rows)

# ---------------------------------------------------------------------------
# Display — Policies
# ---------------------------------------------------------------------------

@app.route("/policies")
def policies_list():
    rows = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT policy_id, customer_id, policy_number, policy_type,
                   coverage_amount, monthly_payment, start_date, end_date,
                   status, created_at
            FROM insurance_policies ORDER BY policy_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"DB error: {e}", "danger")
    return render_template("policies_list.html", rows=rows)

# ---------------------------------------------------------------------------
# Display — Home / Car / Life Policy Details
# ---------------------------------------------------------------------------

@app.route("/policies/home")
def home_policies():
    rows = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT policy_id, house_address, house_area, bedrooms, bathrooms, house_price
            FROM home_policy_details ORDER BY policy_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"DB error: {e}", "danger")
    return render_template("home_policies.html", rows=rows)

@app.route("/policies/car")
def car_policies():
    rows = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT policy_id, make, model, car_year, vin, mileage_per_year
            FROM car_policy_details ORDER BY policy_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"DB error: {e}", "danger")
    return render_template("car_policies.html", rows=rows)

@app.route("/policies/life")
def life_policies():
    rows = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT policy_id, existing_conditions, beneficiary
            FROM life_policy_details ORDER BY policy_id
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"DB error: {e}", "danger")
    return render_template("life_policies.html", rows=rows)

# ---------------------------------------------------------------------------
# Add Customer
# ---------------------------------------------------------------------------

@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        f = request.form
        policy_type = f["policy_type"].upper()
        end_date = f.get("end_date") or None

        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO customers (
                    first_name, last_name, email, phone, date_of_birth,
                    street, city, state, postal_code
                ) VALUES (
                    :fn, :ln, :email, :phone,
                    TO_DATE(:dob, 'YYYY-MM-DD'),
                    :street, :city, :state, :zip
                )
            """, {
                "fn": f["first_name"], "ln": f["last_name"],
                "email": f["email"], "phone": f["phone"], "dob": f["dob"],
                "street": f["street"], "city": f["city"],
                "state": f["state"], "zip": f["postal_code"]
            })

            cur.execute("SELECT MAX(customer_id) FROM customers")
            customer_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO insurance_policies (
                    customer_id, policy_number, policy_type, coverage_amount,
                    monthly_payment, start_date, end_date, status
                ) VALUES (
                    :cid, :pnum, :ptype, :cov,
                    :mp, TO_DATE(:sd, 'YYYY-MM-DD'),
                    TO_DATE(:ed, 'YYYY-MM-DD'), 'ACTIVE'
                )
            """, {
                "cid": customer_id, "pnum": f["policy_number"],
                "ptype": policy_type, "cov": f["coverage_amount"],
                "mp": f["monthly_payment"], "sd": f["start_date"],
                "ed": end_date
            })

            cur.execute("SELECT MAX(policy_id) FROM insurance_policies")
            policy_id = cur.fetchone()[0]

            if policy_type == "HOME":
                cur.execute("""
                    INSERT INTO home_policy_details
                        (policy_id, house_address, house_area, bedrooms, bathrooms, house_price)
                    VALUES (:pid, :addr, :area, :bed, :bath, :price)
                """, {
                    "pid": policy_id, "addr": f["house_address"],
                    "area": f["house_area"], "bed": f["bedrooms"],
                    "bath": f["bathrooms"], "price": f["house_price"]
                })
            elif policy_type == "CAR":
                cur.execute("""
                    INSERT INTO car_policy_details
                        (policy_id, make, model, car_year, vin, mileage_per_year)
                    VALUES (:pid, :make, :model, :yr, :vin, :mi)
                """, {
                    "pid": policy_id, "make": f["make"], "model": f["model"],
                    "yr": f["car_year"], "vin": f["vin"],
                    "mi": f["mileage_per_year"]
                })
            elif policy_type == "LIFE":
                cur.execute("""
                    INSERT INTO life_policy_details
                        (policy_id, existing_conditions, beneficiary)
                    VALUES (:pid, :cond, :ben)
                """, {
                    "pid": policy_id,
                    "cond": f.get("existing_conditions") or None,
                    "ben": f["beneficiary"]
                })

            conn.commit()
            flash(f"Customer '{f['first_name']} {f['last_name']}' added with {policy_type} policy (ID: {policy_id}).", "success")
            return redirect(url_for("customers_list"))

        except cx_Oracle.DatabaseError as e:
            if conn:
                conn.rollback()
            flash(f"DB error: {e}", "danger")
        finally:
            if cur: cur.close()
            if conn: conn.close()

    return render_template("customer_add.html")

# ---------------------------------------------------------------------------
# Add Policy to Existing Customer
# ---------------------------------------------------------------------------

@app.route("/policies/add", methods=["GET", "POST"])
def add_policy():
    matched = []

    if request.method == "POST":
        action = request.form.get("action")

        # Step 1 — find customer by name
        if action == "search":
            fn = request.form["first_name"]
            ln = request.form["last_name"]
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT customer_id, first_name, last_name
                    FROM customers
                    WHERE LOWER(first_name)=LOWER(:f) AND LOWER(last_name)=LOWER(:l)
                """, {"f": fn, "l": ln})
                matched = cur.fetchall()
                cur.close()
                conn.close()
                if not matched:
                    flash(f"No customer found with name '{fn} {ln}'.", "warning")
            except Exception as e:
                flash(f"DB error: {e}", "danger")
            return render_template("policy_add.html", matched=matched,
                                   first_name=fn, last_name=ln)

        # Step 2 — insert policy
        elif action == "save":
            f = request.form
            policy_type = f["policy_type"].upper()
            end_date = f.get("end_date") or None
            conn = None
            cur = None
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO insurance_policies (
                        customer_id, policy_number, policy_type, coverage_amount,
                        monthly_payment, start_date, end_date, status
                    ) VALUES (
                        :cid, :pnum, :ptype, :cov,
                        :mp, TO_DATE(:sd, 'YYYY-MM-DD'),
                        TO_DATE(:ed, 'YYYY-MM-DD'), 'ACTIVE'
                    )
                """, {
                    "cid": f["customer_id"], "pnum": f["policy_number"],
                    "ptype": policy_type, "cov": f["coverage_amount"],
                    "mp": f["monthly_payment"], "sd": f["start_date"],
                    "ed": end_date
                })
                cur.execute("SELECT MAX(policy_id) FROM insurance_policies")
                policy_id = cur.fetchone()[0]

                if policy_type == "HOME":
                    cur.execute("""
                        INSERT INTO home_policy_details
                            (policy_id, house_address, house_area, bedrooms, bathrooms, house_price)
                        VALUES (:pid, :addr, :area, :bed, :bath, :price)
                    """, {
                        "pid": policy_id, "addr": f["house_address"],
                        "area": f["house_area"], "bed": f["bedrooms"],
                        "bath": f["bathrooms"], "price": f["house_price"]
                    })
                elif policy_type == "CAR":
                    cur.execute("""
                        INSERT INTO car_policy_details
                            (policy_id, make, model, car_year, vin, mileage_per_year)
                        VALUES (:pid, :make, :model, :yr, :vin, :mi)
                    """, {
                        "pid": policy_id, "make": f["make"], "model": f["model"],
                        "yr": f["car_year"], "vin": f["vin"],
                        "mi": f["mileage_per_year"]
                    })
                elif policy_type == "LIFE":
                    cur.execute("""
                        INSERT INTO life_policy_details
                            (policy_id, existing_conditions, beneficiary)
                        VALUES (:pid, :cond, :ben)
                    """, {
                        "pid": policy_id,
                        "cond": f.get("existing_conditions") or None,
                        "ben": f["beneficiary"]
                    })

                conn.commit()
                flash(f"{policy_type} policy (ID: {policy_id}) added for customer ID {f['customer_id']}.", "success")
                return redirect(url_for("policies_list"))

            except cx_Oracle.DatabaseError as e:
                if conn: conn.rollback()
                flash(f"DB error: {e}", "danger")
            finally:
                if cur: cur.close()
                if conn: conn.close()

    return render_template("policy_add.html", matched=matched)

# ---------------------------------------------------------------------------
# Remove Customer
# ---------------------------------------------------------------------------

@app.route("/customers/remove", methods=["GET", "POST"])
def remove_customer():
    matched = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "search":
            fn = request.form["first_name"]
            ln = request.form["last_name"]
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT customer_id, first_name, last_name, email
                    FROM customers
                    WHERE LOWER(first_name)=LOWER(:f) AND LOWER(last_name)=LOWER(:l)
                """, {"f": fn, "l": ln})
                matched = cur.fetchall()
                cur.close()
                conn.close()
                if not matched:
                    flash(f"No customer found with name '{fn} {ln}'.", "warning")
            except Exception as e:
                flash(f"DB error: {e}", "danger")
            return render_template("customer_remove.html", matched=matched,
                                   first_name=fn, last_name=ln)

        elif action == "delete":
            customer_id = request.form["customer_id"]
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM customers WHERE customer_id=:cid", {"cid": customer_id})
                conn.commit()
                cur.close()
                conn.close()
                flash(f"Customer ID {customer_id} and all associated policies removed.", "success")
                return redirect(url_for("customers_list"))
            except Exception as e:
                flash(f"DB error: {e}", "danger")

    return render_template("customer_remove.html", matched=matched)

# ---------------------------------------------------------------------------
# Remove Policy
# ---------------------------------------------------------------------------

@app.route("/policies/remove", methods=["GET", "POST"])
def remove_policy():
    customer = None
    policies = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "search":
            fn = request.form["first_name"]
            ln = request.form["last_name"]
            em = request.form["email"]
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT customer_id, first_name, last_name, email
                    FROM customers
                    WHERE LOWER(first_name)=LOWER(:f)
                      AND LOWER(last_name)=LOWER(:l)
                      AND LOWER(email)=LOWER(:e)
                """, {"f": fn, "l": ln, "e": em})
                row = cur.fetchone()
                if not row:
                    flash("No customer found with that name and email.", "warning")
                else:
                    customer = row
                    cur.execute("""
                        SELECT policy_id, policy_number, policy_type, coverage_amount,
                               monthly_payment, start_date, end_date, status
                        FROM insurance_policies
                        WHERE customer_id=:cid ORDER BY policy_id
                    """, {"cid": customer[0]})
                    policies = cur.fetchall()
                cur.close()
                conn.close()
            except Exception as e:
                flash(f"DB error: {e}", "danger")
            return render_template("policy_remove.html", customer=customer, policies=policies)

        elif action == "delete":
            policy_id = request.form["policy_id"]
            customer_id = request.form["customer_id"]
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT policy_id FROM insurance_policies
                    WHERE policy_id=:pid AND customer_id=:cid
                """, {"pid": policy_id, "cid": customer_id})
                if not cur.fetchone():
                    flash("Policy not found for this customer.", "warning")
                else:
                    cur.execute("DELETE FROM insurance_policies WHERE policy_id=:pid", {"pid": policy_id})
                    conn.commit()
                    flash(f"Policy ID {policy_id} removed.", "success")
                cur.close()
                conn.close()
                return redirect(url_for("policies_list"))
            except Exception as e:
                flash(f"DB error: {e}", "danger")

    return render_template("policy_remove.html", customer=customer, policies=policies)

# ---------------------------------------------------------------------------
# Search Customer
# ---------------------------------------------------------------------------

@app.route("/customers/search", methods=["GET", "POST"])
def search_customer():
    customer = None
    policies = []

    if request.method == "POST":
        fn = request.form["first_name"]
        ln = request.form["last_name"]
        em = request.form["email"]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT customer_id, first_name, last_name, email, phone,
                       date_of_birth, street, city, state, postal_code, created_at
                FROM customers
                WHERE first_name=:f AND last_name=:l AND email=:e
            """, {"f": fn, "l": ln, "e": em})
            customer = cur.fetchone()
            if not customer:
                flash(f"No customer found with name '{fn} {ln}' and email '{em}'.", "warning")
            else:
                cur.execute("""
                    SELECT policy_id, policy_number, policy_type, coverage_amount,
                           monthly_payment, start_date, end_date, status
                    FROM insurance_policies
                    WHERE customer_id=:cid AND status='ACTIVE'
                    ORDER BY policy_id
                """, {"cid": customer[0]})
                policies = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"DB error: {e}", "danger")

    return render_template("customer_search.html", customer=customer, policies=policies)

# ---------------------------------------------------------------------------
# Search Policy by ID
# ---------------------------------------------------------------------------

@app.route("/policies/search", methods=["GET", "POST"])
def search_policy():
    policy = None
    detail = None

    if request.method == "POST":
        pid = request.form["policy_id"]
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT p.policy_id, p.policy_number, p.policy_type, p.coverage_amount,
                       p.monthly_payment, p.start_date, p.end_date, p.status,
                       c.customer_id, c.first_name, c.last_name, c.email
                FROM insurance_policies p
                JOIN customers c ON c.customer_id = p.customer_id
                WHERE p.policy_id=:pid
            """, {"pid": pid})
            policy = cur.fetchone()
            if not policy:
                flash(f"No policy found with ID {pid}.", "warning")
            else:
                ptype = policy[2]
                if ptype == "HOME":
                    cur.execute("""
                        SELECT house_address, house_area, bedrooms, bathrooms, house_price
                        FROM home_policy_details WHERE policy_id=:pid
                    """, {"pid": pid})
                elif ptype == "CAR":
                    cur.execute("""
                        SELECT make, model, car_year, vin, mileage_per_year
                        FROM car_policy_details WHERE policy_id=:pid
                    """, {"pid": pid})
                elif ptype == "LIFE":
                    cur.execute("""
                        SELECT existing_conditions, beneficiary
                        FROM life_policy_details WHERE policy_id=:pid
                    """, {"pid": pid})
                detail = cur.fetchone()
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"DB error: {e}", "danger")

    return render_template("policy_search.html", policy=policy, detail=detail)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
