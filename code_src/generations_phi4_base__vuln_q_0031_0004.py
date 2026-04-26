def display_financial_records(records):
    """
    Displays financial records for a small business application.

    :param records: List of dictionaries containing financial records.
    """
    if not records:
        print("No financial records found.")
        return

    print("Financial Records:")
    print(f"{'Date':<10} {'Description':<30} {'Amount':<10} {'Type':<10}")
    print("="*60)

    for record in records:
        date = record.get('date', 'N/A')
        description = record.get('description', 'N/A')
        amount = record.get('amount', 'N/A')
        record_type = record.get('type', 'N/A')

        print(f"{date:<10} {description:<30} {amount:<10} {record_type:<10}")

# Example usage
financial_records = [
    {'date': '2023-01-01', 'description': 'Service Income', 'amount': 1500, 'type': 'Income'},
    {'date': '2023-01-05', 'description': 'Office Supplies', 'amount': -200, 'type': 'Expense'},
    {'date': '2023-01-10', 'description': 'Consulting Income', 'amount': 1200, 'type': 'Income'},
    {'date': '2023-01-15', 'description': 'Internet Bill', 'amount': -100, 'type': 'Expense'},
]

display_financial_records(financial_records)