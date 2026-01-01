import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_data(num_customers=1000, num_transactions=5000):
    print("Generating synthetic data...")

    # --- 1. Generate Customers ---
    customer_ids = np.arange(1001, 1001 + num_customers)

    cities = ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya']
    weights_cities = [0.4, 0.2, 0.15, 0.15, 0.1] # Istanbul is denser

    data_customers = {
        'customer_id': customer_ids,
        'age': np.random.randint(18, 70, size=num_customers),
        'gender': np.random.choice(['M', 'F'], size=num_customers),
        'city': np.random.choice(cities, size=num_customers, p=weights_cities)
    }

    df_customers = pd.DataFrame(data_customers)

    # --- 2. Generate Transactions ---
    # Categories have different spending profiles
    categories = ['Market', 'Giyim', 'Elektronik', 'Restoran', 'Akaryakit']

    transaction_data = []

    start_date = datetime(2023, 1, 1)

    for _ in range(num_transactions):
        cust_id = np.random.choice(customer_ids)

        # Random date within the year
        days_offset = random.randint(0, 365)
        tx_date = start_date + timedelta(days=days_offset)

        category = np.random.choice(categories)

        # Amount depends on category
        if category == 'Elektronik':
            amount = np.random.normal(3000, 1000) # Expensive
        elif category == 'Giyim':
            amount = np.random.normal(800, 300)
        elif category == 'Market':
            amount = np.random.normal(300, 100)
        elif category == 'Akaryakit':
            amount = np.random.normal(600, 100)
        else: # Restoran
            amount = np.random.normal(250, 80)

        # Ensure no negative amounts
        amount = max(10.0, amount)

        transaction_data.append({
            'customer_id': cust_id,
            'transaction_date': tx_date.strftime('%Y-%m-%d'),
            'amount': round(amount, 2),
            'category': category
        })

    df_transactions = pd.DataFrame(transaction_data)

    # Add a transaction_id
    df_transactions['transaction_id'] = np.arange(1, len(df_transactions) + 1)

    # Reorder columns
    df_transactions = df_transactions[['transaction_id', 'customer_id', 'transaction_date', 'amount', 'category']]

    # Save to CSV
    df_customers.to_csv('BankCustomerAnalysis/customers.csv', index=False)
    df_transactions.to_csv('BankCustomerAnalysis/transactions.csv', index=False)

    print(f"Success! Created 'customers.csv' ({len(df_customers)} rows) and 'transactions.csv' ({len(df_transactions)} rows).")

if __name__ == "__main__":
    # Seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    generate_data()
