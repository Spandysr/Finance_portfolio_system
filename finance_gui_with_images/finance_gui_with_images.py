
import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'suma',  # Change this to your actual password
    'database': 'finance_portfolio_db'
}

def connect_db():
    return mysql.connector.connect(**db_config)

def execute_query(query, params):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        print("Database Error:", e)

def load_background(window, image_path):
    bg_image = Image.open(image_path)
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    return bg_label

def submit_data(table, fields, entries):
    data = [entry.get() for entry in entries]
    if '' in data:
        messagebox.showwarning("Input Error", "Please fill all fields")
        return
    placeholders = ", ".join(["%s"] * len(fields))
    query = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
    execute_query(query, tuple(data))
    messagebox.showinfo("Success", f"{table} entry added successfully!")

def create_form(window, title_text, fields, table, image_path):
    window.title(title_text)
    window.geometry("800x600")
    load_background(window, image_path)
    Label(window, text=title_text, font=("Arial", 18, "bold"), bg="white").place(x=20, y=20)
    entries = []
    for i, field in enumerate(fields):
        Label(window, text=field, bg="white").place(x=50, y=80 + i*40)
        entry = Entry(window)
        entry.place(x=200, y=80 + i*40)
        entries.append(entry)
    Button(window, text="Submit", command=lambda: submit_data(table, fields, entries)).place(x=200, y=80 + len(fields)*40)

def open_investor_page():
    window = Toplevel()
    create_form(window, "Investor Management",
                ["InvestorID", "Name", "Email"], "Investor",
                "images/investor_bg.jpg")

def open_asset_page():
    window = Toplevel()
    create_form(window, "Asset Management",
                ["AssetID", "Name", "Type"], "Asset",
                "images/asset_bg.jpg")

def open_portfolio_page():
    window = Toplevel()
    create_form(window, "Portfolio Management",
                ["PortfolioID", "InvestorID", "AssetID"], "Portfolio",
                "images/portfolio.jpg")

def open_investment_page():
    window = Toplevel()
    create_form(window, "Investment Management",
                ["InvestmentID", "PortfolioID", "Amount"], "Investment",
                "images/investment_bg.jpg")

def open_transaction_page():
    window = Toplevel()
    create_form(window, "Transaction Management",
                ["TransactionID", "InvestmentID", "Date", "Amount"], "Transaction",
                "images/transaction_bg.jpg")

# Main GUI Window
root = Tk()
root.title("Finance Portfolio Management System")
root.geometry("800x600")
load_background(root, "images/dashboard.jpg")
Label(root, text="Finance Portfolio Management System", font=("Arial", 20, "bold"), bg="white").place(x=150, y=30)

Button(root, text="Investor", width=20, command=open_investor_page).place(x=300, y=120)
Button(root, text="Asset", width=20, command=open_asset_page).place(x=300, y=180)
Button(root, text="Portfolio", width=20, command=open_portfolio_page).place(x=300, y=240)
Button(root, text="Investment", width=20, command=open_investment_page).place(x=300, y=300)
Button(root, text="Transaction", width=20, command=open_transaction_page).place(x=300, y=360)

root.mainloop()

