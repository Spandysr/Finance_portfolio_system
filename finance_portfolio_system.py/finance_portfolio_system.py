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

def add_investor(name, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Investor (Name, Email) VALUES (%s, %s)", (name, email))
    conn.commit()
    print(f"Investor '{name}' added.")
    cursor.close()
    conn.close()

def add_asset(asset_type, name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Asset (AssetType, Name) VALUES (%s, %s)", (asset_type, name))
    conn.commit()
    print(f"Asset '{name}' added.")
    cursor.close()
    conn.close()

def create_portfolio(investor_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Portfolio (InvestorID, CreatedDate) VALUES (%s, %s)", (investor_id, date.today()))
    conn.commit()
    print(f"Portfolio created for Investor ID {investor_id}.")
    cursor.close()
    conn.close()

def add_investment(portfolio_id, asset_id, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Investment (PortfolioID, AssetID, AmountInvested, DateOfInvestment) VALUES (%s, %s, %s, %s)",
                   (portfolio_id, asset_id, amount, date.today()))
    conn.commit()
    print("Investment added.")
    cursor.close()
    conn.close()

def add_transaction(investment_id, txn_type, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Transaction (InvestmentID, TransactionType, TransactionDate, Amount) VALUES (%s, %s, %s, %s)",
                   (investment_id, txn_type, date.today(), amount))
    conn.commit()
    print(f"{txn_type} transaction recorded.")
    cursor.close()
    conn.close()

def main():
    while True:
        print("\n--- Finance Portfolio Management ---")
        print("1. Add Investor")
        print("2. Add Asset")
        print("3. Create Portfolio")
        print("4. Add Investment")
        print("5. Add Transaction")
        print("6. Exit")

        choice = input("Select option: ")

        if choice == '1':
            name = input("Investor Name: ")
            email = input("Investor Email: ")
            add_investor(name, email)

        elif choice == '2':
            atype = input("Asset Type (e.g., Stock): ")
            name = input("Asset Name: ")
            add_asset(atype, name)

        elif choice == '3':
            investor_id = int(input("Investor ID: "))
            create_portfolio(investor_id)

        elif choice == '4':
            portfolio_id = int(input("Portfolio ID: "))
            asset_id = int(input("Asset ID: "))
            amount = float(input("Amount Invested: "))
            add_investment(portfolio_id, asset_id, amount)

        elif choice == '5':
            investment_id = int(input("Investment ID: "))
            txn_type = input("Transaction Type (Buy/Sell): ")
            amount = float(input("Amount: "))
            add_transaction(investment_id, txn_type, amount)

        elif choice == '6':
            print("Exiting system.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

