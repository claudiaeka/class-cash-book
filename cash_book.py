from datetime import datetime
from typing import List, Dict, Tuple
import json

class CashBook:
    """
    A class to manage cash transactions, track balances, and generate reports.
    """
    
    def __init__(self, initial_balance: float = 0):
        """
        Initialize the cash book with an optional initial balance.
        
        Args:
            initial_balance (float): Starting balance in the cash book
        """
        self.transactions: List[Dict] = []
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
    
    def record_transaction(self, amount: float, transaction_type: str, description: str = "", date: str = None) -> Dict:
        """
        Record a cash transaction (income or expense).
        
        Args:
            amount (float): Transaction amount
            transaction_type (str): 'debit' (expense) or 'credit' (income)
            description (str): Description of the transaction
            date (str): Transaction date in 'YYYY-MM-DD' format. Defaults to today.
        
        Returns:
            Dict: The recorded transaction details
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if transaction_type.lower() not in ['debit', 'credit']:
            raise ValueError("Transaction type must be 'debit' or 'credit'")
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Date must be in 'YYYY-MM-DD' format")
        
        # Update balance
        if transaction_type.lower() == 'credit':
            self.current_balance += amount
        else:  # debit
            if self.current_balance < amount:
                raise ValueError(f"Insufficient balance. Current balance: {self.current_balance}")
            self.current_balance -= amount
        
        # Record transaction
        transaction = {
            'id': len(self.transactions) + 1,
            'date': date,
            'type': transaction_type.lower(),
            'amount': amount,
            'description': description,
            'balance_after': self.current_balance
        }
        
        self.transactions.append(transaction)
        return transaction
    
    def get_balance(self) -> float:
        """
        Get the current cash balance.
        
        Returns:
            float: Current balance
        """
        return self.current_balance
    
    def get_total_credits(self) -> float:
        """
        Calculate total income (credits).
        
        Returns:
            float: Sum of all credit transactions
        """
        return sum(txn['amount'] for txn in self.transactions if txn['type'] == 'credit')
    
    def get_total_debits(self) -> float:
        """
        Calculate total expenses (debits).
        
        Returns:
            float: Sum of all debit transactions
        """
        return sum(txn['amount'] for txn in self.transactions if txn['type'] == 'debit')
    
    def get_transactions(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """
        Get transactions within a date range.
        
        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
        
        Returns:
            List[Dict]: Filtered transactions
        """
        filtered = self.transactions
        
        if start_date:
            filtered = [t for t in filtered if t['date'] >= start_date]
        
        if end_date:
            filtered = [t for t in filtered if t['date'] <= end_date]
        
        return filtered
    
    def generate_report(self, start_date: str = None, end_date: str = None) -> str:
        """
        Generate a detailed cash book report.
        
        Args:
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format
        
        Returns:
            str: Formatted report
        """
        filtered_transactions = self.get_transactions(start_date, end_date)
        
        report = "=" * 80 + "\n"
        report += "CASH BOOK REPORT\n"
        report += "=" * 80 + "\n\n"
        
        if start_date or end_date:
            report += f"Period: {start_date or 'Start'} to {end_date or 'End'}\n\n"
        
        report += f"Initial Balance: ${self.initial_balance:.2f}\n"
        report += f"Current Balance: ${self.current_balance:.2f}\n\n"
        
        report += "-" * 80 + "\n"
        report += f"{'ID':<5} {'Date':<12} {'Type':<8} {'Amount':<12} {'Description':<25} {'Balance':<12}\n"
        report += "-" * 80 + "\n"
        
        for txn in filtered_transactions:
            txn_type = txn['type'].upper()
            report += f"{txn['id']:<5} {txn['date']:<12} {txn_type:<8} ${txn['amount']:<11.2f} {txn['description']:<25} ${txn['balance_after']:<11.2f}\n"
        
        report += "-" * 80 + "\n"
        
        total_credits = sum(t['amount'] for t in filtered_transactions if t['type'] == 'credit')
        total_debits = sum(t['amount'] for t in filtered_transactions if t['type'] == 'debit')
        
        report += f"\nTotal Credits (Income):  ${total_credits:.2f}\n"
        report += f"Total Debits (Expenses): ${total_debits:.2f}\n"
        report += f"Net Change:             ${total_credits - total_debits:.2f}\n"
        report += f"\nFinal Balance:          ${self.current_balance:.2f}\n"
        report += "=" * 80 + "\n"
        
        return report
    
    def save_to_json(self, filename: str) -> None:
        """
        Save cash book data to a JSON file.
        
        Args:
            filename (str): Name of the file to save to
        """
        data = {
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'transactions': self.transactions,
            'saved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Cash book saved to {filename}")
    
    def load_from_json(self, filename: str) -> None:
        """
        Load cash book data from a JSON file.
        
        Args:
            filename (str): Name of the file to load from
        """
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.initial_balance = data['initial_balance']
        self.current_balance = data['current_balance']
        self.transactions = data['transactions']
        
        print(f"Cash book loaded from {filename}")
    
    def get_summary(self) -> Dict:
        """
        Get a summary of the cash book.
        
        Returns:
            Dict: Summary statistics
        """
        return {
            'initial_balance': self.initial_balance,
            'current_balance': self.current_balance,
            'total_credits': self.get_total_credits(),
            'total_debits': self.get_total_debits(),
            'transaction_count': len(self.transactions),
            'net_change': self.current_balance - self.initial_balance
        }


# Example usage
if __name__ == "__main__":
    # Create a cash book with initial balance of $1000
    cash_book = CashBook(initial_balance=1000)
    
    # Record some transactions
    print("Recording transactions...\n")
    cash_book.record_transaction(500, 'credit', 'Salary deposit')
    cash_book.record_transaction(150, 'debit', 'Groceries')
    cash_book.record_transaction(75, 'debit', 'Gas')
    cash_book.record_transaction(200, 'credit', 'Freelance work')
    cash_book.record_transaction(50, 'debit', 'Utilities')
    
    # Display the report
    print(cash_book.generate_report())
    
    # Get summary
    print("\nSummary:")
    summary = cash_book.get_summary()
    for key, value in summary.items():
        if isinstance(value, float):
            print(f"{key}: ${value:.2f}")
        else:
            print(f"{key}: {value}")
    
    # Save to JSON
    cash_book.save_to_json('cash_book_data.json')
