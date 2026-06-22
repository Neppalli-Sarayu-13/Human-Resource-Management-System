from flask import Flask, render_template, request, redirect, session
from db import get_connection

app = Flask(__name__)
app.secret_key = "secret"

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    username = request.form['username']
    password = request.form['password']
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT UserID, UserName, Role FROM users WHERE UserName=? AND Password=?",
        (username, password)
    )
    user = cursor.fetchone()
    if user:
        session['UserID'] = user[0]
        session['username'] = user[1]
        session['role'] = user[2]
        cursor.execute(
            "UPDATE users SET Is_logged_in=1 WHERE UserID=?",
            (user[0],)
        )
        conn.commit()
        conn.close()
        if user[2] == "admin":
            return redirect("/admin_dashboard")
        else:
            return redirect("/employee_dashboard")
    conn.close()
    return render_template("index.html", error="Invalid username or password")

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/login")
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE Role = 'employee'
    """)
    employee_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE Role = 'employee' AND Is_logged_in = 1
    """)
    active_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT UserID, UserName, Role, Email, Phoneno, Salary, join_Date
        FROM users
        WHERE Role = 'employee'
    """)
    all_employees = cursor.fetchall()

    cursor.execute("""
        SELECT UserID, UserName, Role
        FROM users
        WHERE Role = 'employee' AND Is_logged_in = 1
    """)
    active_employees = cursor.fetchall()
    conn.close()
    return render_template("admin_dashboard.html", username=session.get("username"), employee_count=employee_count, active_count=active_count, users=all_employees, active_users=active_employees)

@app.route("/employee_dashboard")
def employee_dashboard():
    if "UserID" not in session:
        return redirect("/login")
    if session.get("role") != "employee":
        return "Access Denied"
    return render_template(
        "employee_dashboard.html",
        username=session.get("username")
    )

@app.route('/logout')
def logout():
    user_id = session.get('UserID')
    if user_id:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET Is_logged_in=0 WHERE UserID=?",
            (user_id,)
        )
        conn.commit()
        conn.close()
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)