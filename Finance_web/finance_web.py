from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from datetime import date
import re
import random
import os
from dotenv import load_dotenv

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="suma",
    database="finance_portfolio_db"
)

load_dotenv()

# Flask App
app = Flask(__name__)
app.secret_key = 'super_secret_key'

# MySQL DB config from environment variables
db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

# Connect to DB
def connect_db():
    return mysql.connector.connect(**db_config)

# --- Routes ---

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
            conn = connect_db()
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

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    message = None

    if request.method == 'POST':
        investor_id = request.form['investor_id']
        name = request.form['name']
        email = request.form['email']

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error = "Invalid email format. Please use example@domain.com."
        else:
            cursor = db.cursor()
            # Check if ID already exists
            cursor.execute("SELECT * FROM Investor WHERE InvestorID = %s", (investor_id,))
            if cursor.fetchone():
                error = "Investor ID already exists!"
            else:
                cursor.execute("INSERT INTO Investor (InvestorID, Name, Email) VALUES (%s, %s, %s)",
                               (investor_id, name, email))
                db.commit()
                message = "Registration successful! You can now login."

    return render_template("signup.html", error=error, message=message)

@app.route('/investor', methods=['GET', 'POST'])
def investor():
    if request.method == 'POST':
        investor_id = request.form['InvestorID']
        name = request.form['Name']
        email = request.form['Email']
        try:
            conn = connect_db()
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

# --- Backend Helper Functions ---

def add_investor(name, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Investor (Name, Email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()

def add_asset(asset_type, name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Asset (AssetType, Name) VALUES (%s, %s)", (asset_type, name))
    conn.commit()
    cursor.close()
    conn.close()

def create_portfolio(investor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Portfolio (InvestorID, CreatedDate) VALUES (%s, %s)", (investor_id, date.today()))
    conn.commit()
    cursor.close()
    conn.close()

def add_investment(portfolio_id, asset_id, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Investment (PortfolioID, AssetID, AmountInvested, DateOfInvestment) VALUES (%s, %s, %s, %s)",
                   (portfolio_id, asset_id, amount, date.today()))
    conn.commit()
    cursor.close()
    conn.close()

def add_transaction(investment_id, txn_type, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Transaction (InvestmentID, TransactionType, TransactionDate, Amount) VALUES (%s, %s, %s, %s)",
                   (investment_id, txn_type, date.today(), amount))
    conn.commit()
    cursor.close()
    conn.close()

# --- Run locally ---
if __name__ == '__main__':
    app.run(debug=True)

