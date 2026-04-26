import pandas as pd
import matplotlib.pyplot as plt

def display_financial_records(file_path):
    # Read the CSV file into a DataFrame
    try:
        financial_records = pd.read_csv(file_path)
        print("Financial Records:")
        print(financial_records)
        
        # Display the data in a table
        print("\nTable of Financial Records:")
        print(financial_records.to_string(index=False))
        
        # Optional: Basic visualization
        plt.figure(figsize=(10, 6))
        financial_records.plot(kind='bar', x='Date', y='Amount', title='Financial Records')
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.show()
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_path = 'financial_records.csv'
display_financial_records(file_path)