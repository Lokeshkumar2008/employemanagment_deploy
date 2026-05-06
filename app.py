from flask import Flask, render_template, redirect, request, session, flash
import random
import mysql.connector
import smtplib
from email.message import EmailMessage
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = "abc@123"

# ---------------- DB CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lokesh@123",
        database="company"
    )

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('login.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, password, role)
        )

        con.commit()
        cur.close()
        con.close()

        flash("Registered successfully!", "success")
        return redirect('/')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cur.fetchone()

        cur.close()
        con.close()

        if user:
            session["admin"] = username
            flash("Login successful!", "success")
            return redirect('/view')
        else:
            flash("Invalid username or password", "danger")
            return redirect('/login')   # 🔥 FIX HERE ALSO

    return render_template('login.html')   # 🔥 VERY IMPORTANT

#----------------dashboard or view -----------------------
@app.route('/view')
def view():

    if "admin" not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()

    # 🔍 SEARCH
    search = request.args.get('search')

    if search:
        cursor.execute(
            "SELECT * FROM employee WHERE ename LIKE %s",
            ('%' + search + '%',)
        )
    else:
        cursor.execute("SELECT * FROM employee")

    employees = cursor.fetchall()

    # 🔢 COUNTS (keep these AFTER search or before — both fine)
    cursor.execute("SELECT COUNT(*) FROM employee")
    total_employees = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT edept) FROM employee")
    total_departments = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(esalary) FROM employee")
    avg_salary = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(esalary) FROM employee")
    total_salary = cursor.fetchone()[0] or 0
    
    conn.close()

    return render_template(
        'dashboard.html',
        employees=employees,
        total_employees=total_employees,
        total_departments=total_departments,
        avg_salary=int(avg_salary),
        total_salary=total_salary
    )
# ---------------- ADD ----------------

@app.route('/add_employee', methods=['GET', 'POST'])
def Add_employee():
    if "admin" not in session:
        flash("Login required!", "warning")
        return redirect('/')

    if request.method == 'POST':
        data = (
            request.form['ename'],
            request.form['edept'],
            request.form['esalary'],
            request.form['ephone']
        )

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO employee (ename, edept, esalary, ephone) VALUES (%s, %s, %s, %s)",
            data
        )

        con.commit()
        cur.close()
        con.close()

        flash("Employee added successfully!", "success")
        return redirect('/view')

    return render_template('add_employee.html')

# ---------------- EDIT ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if "admin" not in session:
        flash("Login required!", "warning")
        return redirect('/')

    con = get_connection()
    cur = con.cursor()

    if request.method == 'POST':
        data = (
            request.form['ename'],
            request.form['edept'],
            request.form['esalary'],
            request.form['ephone'],
            id
        )

        cur.execute("""
            UPDATE employee
            SET ename=%s, edept=%s, esalary=%s, ephone=%s
            WHERE eid=%s
        """, data)

        con.commit()
        cur.close()
        con.close()

        flash("Employee updated successfully!", "success")
        return redirect('/view')

    cur.execute("SELECT * FROM employee WHERE eid=%s", (id,))
    emp = cur.fetchone()

    cur.close()
    con.close()

    return render_template('edit_employee.html', emp=emp)

# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete_employee(id):
    if "admin" not in session:
        flash("Login required!", "warning")
        return redirect('/')

    con = get_connection()
    cur = con.cursor()

    cur.execute("DELETE FROM employee WHERE eid=%s", (id,))
    con.commit()

    cur.close()
    con.close()

    flash("Employee deleted successfully!", "warning")
    return redirect('/view')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def Logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect('/')

# ---------------- CONTACT ----------------
@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        reason = request.form.get('reason')

        sender_email = "lokeshkumarloki580@gmail.com"
        app_password = "ikvc zezm epcc icfa"
        receiver_email = "kmahendra1891@gmail.com"

        msg = EmailMessage()
        msg['Subject'] = "Contact Message"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        msg.set_content(f"""
Name: {name}
Phone: {phone}
Email: {email}
Reason: {reason}
""")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, app_password)
                smtp.send_message(msg)

            flash("Message sent successfully!", "success")
            return redirect('/contact')

        except Exception:
            flash("Something went wrong!", "danger")
            return redirect('/contact')

    return render_template('contact.html')

# ---------------- FORGOT PASSWORD ----------------
otp_store = {}

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == "POST":
        email = request.form["email"]

        con = get_connection()
        cur = con.cursor(buffered=True)

        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        cur.close()
        con.close()
        user = cur.fetchone()
        cur.close()
        con.close()

        if user:
            otp = random.randint(100000, 999999)
            otp_store[email] = otp

            sender_email = "lokeshkumarloki580@gmail.com"
            app_password = "ikvc zezm epcc icfa"

            msg = EmailMessage()
            msg['Subject'] = "OTP Verification"
            msg['From'] = sender_email
            msg['To'] = email
            msg.set_content(f"Your OTP is: {otp}")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email, app_password)
                smtp.send_message(msg)

            session['reset_email'] = email
            return redirect('/verify')

        flash("Email not found", "danger")

    return render_template("forgotpassword.html")

# ---------------- VERIFY ----------------
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == "POST":
        user_otp = int(request.form["otp"])
        email = session.get("reset_email")

        if email in otp_store and otp_store[email] == user_otp:
            return redirect('/reset')

        flash("Invalid OTP", "danger")

    return render_template("verify.html")

# ---------------- RESET ----------------
@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == "POST":
        password = request.form.get("password")
        email = session.get("reset_email")

        new_password = generate_password_hash(password)

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "UPDATE users SET password=%s WHERE email=%s",
            (new_password, email)
        )

        con.commit()
        cur.close()
        con.close()

        otp_store.pop(email, None)
        session.pop("reset_email", None)

        flash("Password updated successfully!", "success")
        return redirect('/')

    return render_template("reset.html")

# ---------------- ABOUT ----------------
@app.route('/about')
def about():
    return render_template('about.html')

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)