import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'suma',
    'database': 'finance_portfolio_db'
}

def connect_db():
    return mysql.connector.connect(**db_config)

def execute_query(query, params):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

root = tk.Tk()
root.title("Finance Portfolio Management System")

def add_investor():
    def submit():
        name = entry_name.get()
        email = entry_email.get()
        execute_query("INSERT INTO Investor (Name, Email) VALUES (%s, %s)", (name, email))
        messagebox.showinfo("Success", f"Investor '{name}' added.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Add Investor")
    tk.Label(window, text="Name").pack()
    entry_name = tk.Entry(window)
    entry_name.pack()
    tk.Label(window, text="Email").pack()
    entry_email = tk.Entry(window)
    entry_email.pack()
    tk.Button(window, text="Submit", command=submit).pack()

def add_asset():
    def submit():
        asset_type = entry_type.get()
        name = entry_name.get()
        execute_query("INSERT INTO Asset (AssetType, Name) VALUES (%s, %s)", (asset_type, name))
        messagebox.showinfo("Success", f"Asset '{name}' added.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Add Asset")
    tk.Label(window, text="Asset Type").pack()
    entry_type = tk.Entry(window)
    entry_type.pack()
    tk.Label(window, text="Name").pack()
    entry_name = tk.Entry(window)
    entry_name.pack()
    tk.Button(window, text="Submit", command=submit).pack()

def create_portfolio():
    def submit():
        investor_id = int(entry_investor_id.get())
        execute_query("INSERT INTO Portfolio (InvestorID, CreatedDate) VALUES (%s, %s)", (investor_id, date.today()))
        messagebox.showinfo("Success", f"Portfolio created for Investor ID {investor_id}.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Create Portfolio")
    tk.Label(window, text="Investor ID").pack()
    entry_investor_id = tk.Entry(window)
    entry_investor_id.pack()
    tk.Button(window, text="Submit", command=submit).pack()

def add_investment():
    def submit():
        portfolio_id = int(entry_portfolio_id.get())
        asset_id = int(entry_asset_id.get())
        amount = float(entry_amount.get())
        execute_query(
            "INSERT INTO Investment (PortfolioID, AssetID, AmountInvested, DateOfInvestment) VALUES (%s, %s, %s, %s)",
            (portfolio_id, asset_id, amount, date.today())
        )
        messagebox.showinfo("Success", "Investment added.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Add Investment")
    tk.Label(window, text="Portfolio ID").pack()
    entry_portfolio_id = tk.Entry(window)
    entry_portfolio_id.pack()
    tk.Label(window, text="Asset ID").pack()
    entry_asset_id = tk.Entry(window)
    entry_asset_id.pack()
    tk.Label(window, text="Amount Invested").pack()
    entry_amount = tk.Entry(window)
    entry_amount.pack()
    tk.Button(window, text="Submit", command=submit).pack()

def add_transaction():
    def submit():
        investment_id = int(entry_investment_id.get())
        txn_type = entry_type.get()
        amount = float(entry_amount.get())
        execute_query(
            "INSERT INTO Transaction (InvestmentID, TransactionType, TransactionDate, Amount) VALUES (%s, %s, %s, %s)",
            (investment_id, txn_type, date.today(), amount)
        )
        messagebox.showinfo("Success", f"{txn_type} transaction added.")
        window.destroy()

    window = tk.Toplevel(root)
    window.title("Add Transaction")
    tk.Label(window, text="Investment ID").pack()
    entry_investment_id = tk.Entry(window)
    entry_investment_id.pack()
    tk.Label(window, text="Transaction Type (Buy/Sell)").pack()
    entry_type = tk.Entry(window)
    entry_type.pack()
    tk.Label(window, text="Amount").pack()
    entry_amount = tk.Entry(window)
    entry_amount.pack()
    tk.Button(window, text="Submit", command=submit).pack()

tk.Button(root, text="Add Investor", width=30, command=add_investor).pack(pady=5)
tk.Button(root, text="Add Asset", width=30, command=add_asset).pack(pady=5)
tk.Button(root, text="Create Portfolio", width=30, command=create_portfolio).pack(pady=5)
tk.Button(root, text="Add Investment", width=30, command=add_investment).pack(pady=5)
tk.Button(root, text="Add Transaction", width=30, command=add_transaction).pack(pady=5)
tk.Button(root, text="Exit", width=30, command=root.destroy).pack(pady=5)

root.mainloop()

