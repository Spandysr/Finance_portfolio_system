from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'finance_portfolio_db'
}

def connect_db():
    return mysql.connector.connect(**db_config)

# ---------- USER AUTH ----------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        investor_id = request.form['investor_id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Investor WHERE Email=%s", (email,))
            if cursor.fetchone():
                flash("Email already registered", "warning")
            else:
                cursor.execute("INSERT INTO Investor (InvestorID, Name, Email, Password) VALUES (%s, %s, %s, %s)",
                               (investor_id, name, email, password))
                conn.commit()
                flash("Signup successful! Please login.", "success")
                return redirect(url_for('login'))
        except Exception as e:
            flash(str(e), "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Investor WHERE Email=%s AND Password=%s", (email, password))
            user = cursor.fetchone()
            if user:
                session['user'] = user['Name']
                session['investor_id'] = user['InvestorID']
                flash("Logged in successfully!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials", "danger")
        except Exception as e:
            flash(str(e), "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for('login'))

# ---------- DASHBOARD ----------
tips = [
    "Invest regularly to benefit from compounding.",
    "Diversify your portfolio to manage risk.",
    "Review your goals periodically.",
    "Keep emergency funds separately."
]

words = [
    ("Asset", "A resource with economic value."),
    ("Equity", "Ownership in a company."),
    ("Inflation", "Rate at which prices increase."),
    ("Portfolio", "Collection of financial assets."),
]

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    index = datetime.datetime.now().day % len(tips)
    today_tip = tips[index]
    today_word, meaning = words[index]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT AssetType, COUNT(*) FROM Asset GROUP BY AssetType")
    asset_data = cursor.fetchall()
    cursor.close()
    conn.close()

    types = [row[0] for row in asset_data]
    counts = [row[1] for row in asset_data]

    return render_template('dashboard.html',
                           user=session['user'],
                           tip=today_tip,
                           word=today_word,
                           meaning=meaning,
                           chart_labels=types,
                           chart_values=counts)

# ---------- PAGES ----------
@app.route('/investor', methods=['GET', 'POST'])
def investor():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        investor_id = request.form['investor_id']
        name = request.form['name']
        email = request.form['email']
        password = request.form.get('password', 'defaultpass')
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Investor (InvestorID, Name, Email, Password) VALUES (%s, %s, %s, %s)",
                           (investor_id, name, email, password))
            conn.commit()
            flash("Investor added successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('investor.html')

@app.route('/asset', methods=['GET', 'POST'])
def asset():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        asset_type = request.form['asset_type']
        name = request.form['name']
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Asset (AssetType, Name) VALUES (%s, %s)",
                           (asset_type, name))
            conn.commit()
            flash("Asset added successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('asset.html')

@app.route('/investment', methods=['GET', 'POST'])
def investment():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        portfolio_id = request.form['portfolio_id']
        asset_id = request.form['asset_id']
        amount = request.form['amount']
        date = request.form['date']
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Investment (PortfolioID, AssetID, AmountInvested, DateOfInvestment) VALUES (%s, %s, %s, %s)",
                           (portfolio_id, asset_id, amount, date))
            conn.commit()
            flash("Investment recorded", "success")
        except Exception as e:
            flash(str(e), "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('investment.html')

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        investment_id = request.form['investment_id']
        transaction_type = request.form['transaction_type']
        date = request.form['date']
        amount = request.form['amount']
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Transaction (InvestmentID, TransactionType, TransactionDate, Amount) VALUES (%s, %s, %s, %s)",
                           (investment_id, transaction_type, date, amount))
            conn.commit()
            flash("Transaction recorded", "success")
        except Exception as e:
            flash(str(e), "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template('transaction.html')

@app.route('/advisor')
def advisor():
    if 'user' not in session:
        return redirect(url_for('login'))

    recommendation = ""
    amount = request.args.get('amount')
    if amount:
        amount = float(amount)
        if amount < 10000:
            recommendation = "Consider investing in low-risk fixed deposits or mutual funds."
        elif amount < 50000:
            recommendation = "Diversify across stocks and bonds."
        else:
            recommendation = "You can explore equity, real estate, and international funds."

    return render_template('advisor.html', recommendation=recommendation)

if __name__ == '__main__':
    app.run(debug=True)

