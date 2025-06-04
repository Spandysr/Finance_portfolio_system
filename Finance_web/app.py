from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from datetime import date
import re
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# MySQL config from .env
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'suma'),
    'database': os.getenv('DB_NAME', 'finance_portfolio_db')
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

# Daily random word/thought
WORDS = ["Investment", "Diversification", "SIP", "ETF", "Risk"]
THOUGHTS = [
    "A penny saved is a penny earned.",
    "Invest for the long term, not the short term.",
    "Don’t put all your eggs in one basket.",
    "Start early to reap the power of compounding."
]

def get_daily_items():
    return random.choice(WORDS), random.choice(THOUGHTS)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.com$", email):
            flash("Invalid email format", "danger")
            return redirect(url_for('login'))

        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Investor WHERE Email=%s AND InvestorID=%s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user'] = user['Name']
            session['user_id'] = user['InvestorID']
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        investor_id = request.form['investor_id']
        name = request.form['name']
        email = request.form['email']

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format", "danger")
        else:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Investor WHERE InvestorID=%s", (investor_id,))
            if cursor.fetchone():
                flash("Investor ID already exists", "danger")
            else:
                cursor.execute("INSERT INTO Investor (InvestorID, Name, Email) VALUES (%s, %s, %s)", (investor_id, name, email))
                conn.commit()
                flash("Signup successful! Please login.", "success")
            cursor.close()
            conn.close()
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    word, thought = get_daily_items()
    return render_template('dashboard.html', user=session['user'], word=word, thought=thought)

@app.route('/advisor', methods=['GET', 'POST'])
def advisor():
    if 'user' not in session:
        return redirect(url_for('login'))
    suggestion = None
    if request.method == 'POST':
        amount = float(request.form['amount'])
        tips = [
            "Start with mutual funds or SIPs.",
            "Explore diversified equity mutual funds.",
            "Consider stocks, bonds, and ETFs based on your profile."
        ]
        suggestion = random.choice(tips)
    return render_template('advisor.html', suggestion=suggestion)

@app.route('/investor', methods=['GET', 'POST'])
def investor():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        investor_id = request.form['investor_id']
        name = request.form['name']
        email = request.form['email']
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Investor (InvestorID, Name, Email) VALUES (%s, %s, %s)", (investor_id, name, email))
            conn.commit()
            flash("Investor added successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('investor.html')

@app.route('/investment', methods=['GET', 'POST'])
def investment():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        portfolio_id = request.form['portfolio_id']
        asset_id = request.form['asset_id']
        amount = request.form['amount']
        date_of_inv = request.form['date']
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Investment (PortfolioID, AssetID, AmountInvested, DateOfInvestment) VALUES (%s, %s, %s, %s)", (portfolio_id, asset_id, amount, date_of_inv))
            conn.commit()
            flash("Investment added successfully.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template("investment.html")

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        investment_id = request.form['investment_id']
        txn_type = request.form['transaction_type']
        txn_date = request.form['transaction_date']
        amount = request.form['amount']
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Transaction (InvestmentID, TransactionType, TransactionDate, Amount) VALUES (%s, %s, %s, %s)", (investment_id, txn_type, txn_date, amount))
            conn.commit()
            flash("Transaction successful.", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template("transaction.html")

@app.route('/goals')
def goals():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("goals.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

