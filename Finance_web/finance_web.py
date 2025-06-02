from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import re
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Configure MySQL database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'suma',
    'database': 'finance_portfolio_db'
}

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.com$", email):
            flash("Invalid email format")
            return redirect(url_for('login'))
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Investor WHERE Email=%s AND InvestorID=%s", (email, password))
            user = cursor.fetchone()
            if user:
                session['user'] = user['Name']
                flash("Logged in successfully!", "success")
                return redirect(url_for('index'))
            else:
                flash("Login failed: Invalid credentials", "danger")
        except Exception as e:
            flash(str(e), "danger")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return render_template('login.html')

@app.route('/investor', methods=['GET', 'POST'])
def investor():
    if request.method == 'POST':
        investor_id = request.form['InvestorID']
        name = request.form['Name']
        email = request.form['Email']
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Investor (InvestorID, Name, Email) VALUES (%s, %s, %s)", (investor_id, name, email))
            conn.commit()
            flash("Investor added successfully!", "success")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    return render_template('investor.html')

@app.route('/advisor', methods=['GET', 'POST'])
def advisor():
    suggestion = None
    if request.method == 'POST':
        amount = float(request.form['amount'])
        tips = [
            "Diversify your investments.",
            "Consider low-cost index funds.",
            "Review your portfolio quarterly.",
            "Invest in SIPs for consistent growth.",
            "Avoid timing the market."
        ]
        suggestion = random.choice(tips)
    return render_template('advisor.html', suggestion=suggestion)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

