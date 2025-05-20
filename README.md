# Finance_portfolio_system

# Finance Portfolio Management System

This is a basic Finance Portfolio Management System built using Python and MySQL. It allows you to manage investors, assets, portfolios, investments, and transactions.

## 📁 Contents

- `finance_portfolio_db.sql` — SQL script to create and initialize the database schema.
- `finance_portfolio_system.py` — Console-based application to interact with the database.
- `finance_gui.py` — GUI-based interface using Tkinter for ease of use.

---

## 🛠 Requirements

- Python 3.x
- MySQL Server
- Python Packages:
  - mysql-connector-python
  - tkinter (comes pre-installed with Python)

Install the MySQL connector with:

```bash
pip install mysql-connector-python
```

---

## 🧱 Database Setup

1. Open MySQL Workbench or any MySQL client.
2. Run the SQL file:

```sql
SOURCE path/to/finance_portfolio_db.sql;
```

This will create a database named `finance_portfolio_db` with required tables.

---

## ▶ Running the Application

### Console Version

```bash
python finance_portfolio_system.py
```

This version uses a terminal-based menu.

### GUI Version

```bash
python finance_gui.py
```

This launches a graphical interface built using Tkinter.

---

## 🧩 Features

- **Investor Management** — Add investors with name and email.
- **Asset Management** — Add assets like stocks, bonds, etc.
- **Portfolio Creation** — Create portfolios linked to investors.
- **Investment Tracking** — Track asset investments by portfolio.
- **Transaction Logs** — Record buy/sell actions with dates and amounts.

---

## 📝 Notes

- Make sure the MySQL server is running.
- Update your MySQL credentials in both `.py` files (`db_config` dictionary).

---

## 📧 Support

For questions, feel free to reach out to the project contributor.


