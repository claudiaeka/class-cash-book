"""
Example usage demonstrating all features of the CashBook class.
"""

from cash_book import CashBook

def main():
    print("=" * 80)
    print("CLASH CASH BOOK - EXAMPLE USAGE")
    print("=" * 80)
    
    # 1. Create a cash book with initial balance
    print("\n1. Creating a cash book with initial balance of $5000...")
    cash_book = CashBook(initial_balance=5000)
    print(f"✓ Cash book created. Initial balance: ${cash_book.get_balance()}")
    
    # 2. Record various transactions
    print("\n2. Recording transactions...")
    transactions = [
        (2500, 'credit', 'Monthly Salary', '2026-05-01'),
        (800, 'debit', 'Rent Payment', '2026-05-02'),
        (200, 'debit', 'Groceries', '2026-05-05'),
        (150, 'debit', 'Utilities', '2026-05-07'),
        (300, 'credit', 'Freelance Project', '2026-05-10'),
        (75, 'debit', 'Gas', '2026-05-12'),
        (500, 'credit', 'Bonus', '2026-05-15'),
        (120, 'debit', 'Internet Bill', '2026-05-18'),
        (50, 'debit', 'Coffee', '2026-05-19'),
    ]
    
    for amount, trans_type, description, date in transactions:
        txn = cash_book.record_transaction(amount, trans_type, description, date)
        print(f"✓ {description}: ${amount} ({trans_type.upper()}) - New Balance: ${txn['balance_after']:.2f}")
    
    # 3. Display current balance
    print(f"\n3. Current Balance: ${cash_book.get_balance():.2f}")
    
    # 4. Get summary statistics
    print("\n4. Financial Summary:")
    summary = cash_book.get_summary()
    print(f"   Initial Balance:     ${summary['initial_balance']:.2f}")
    print(f"   Current Balance:     ${summary['current_balance']:.2f}")
    print(f"   Total Credits:       ${summary['total_credits']:.2f}")
    print(f"   Total Debits:        ${summary['total_debits']:.2f}")
    print(f"   Net Change:          ${summary['net_change']:.2f}")
    print(f"   Total Transactions:  {summary['transaction_count']}")
    
    # 5. Generate full report
    print("\n5. Full Cash Book Report:")
    print(cash_book.generate_report())
    
    # 6. Generate report for specific date range
    print("\n6. Report for May 1-15, 2026:")
    print(cash_book.generate_report(
        start_date='2026-05-01',
        end_date='2026-05-15'
    ))
    
    # 7. Get all transactions
    print("\n7. All Transactions:")
    for txn in cash_book.transactions:
        print(f"   ID {txn['id']}: {txn['date']} - {txn['type'].upper():6} ${txn['amount']:8.2f} - {txn['description']}")
    
    # 8. Save to JSON
    print("\n8. Saving cash book to JSON...")
    cash_book.save_to_json('cash_book_example.json')
    print("✓ Cash book saved to 'cash_book_example.json'")
    
    # 9. Load from JSON
    print("\n9. Loading cash book from JSON...")
    loaded_book = CashBook()
    loaded_book.load_from_json('cash_book_example.json')
    print(f"✓ Cash book loaded. Balance: ${loaded_book.get_balance():.2f}")
    
    # 10. Error handling examples
    print("\n10. Error Handling Examples:")
    
    # Try insufficient balance
    try:
        cash_book.record_transaction(50000, 'debit', 'Large withdrawal')
    except ValueError as e:
        print(f"   ✗ Error caught: {e}")
    
    # Try invalid transaction type
    try:
        cash_book.record_transaction(100, 'invalid', 'Bad type')
    except ValueError as e:
        print(f"   ✗ Error caught: {e}")
    
    # Try negative amount
    try:
        cash_book.record_transaction(-100, 'credit', 'Negative amount')
    except ValueError as e:
        print(f"   ✗ Error caught: {e}")
    
    # Try invalid date format
    try:
        cash_book.record_transaction(100, 'credit', 'Bad date', '05/19/2026')
    except ValueError as e:
        print(f"   ✗ Error caught: {e}")
    
    print("\n" + "=" * 80)
    print("EXAMPLE COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()
