"""
Unit tests for the CashBook class.
"""

import unittest
import os
from cash_book import CashBook


class TestCashBook(unittest.TestCase):
    """Test suite for CashBook class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.cash_book = CashBook(initial_balance=1000)
    
    def test_initialization(self):
        """Test CashBook initialization"""
        self.assertEqual(self.cash_book.initial_balance, 1000)
        self.assertEqual(self.cash_book.current_balance, 1000)
        self.assertEqual(len(self.cash_book.transactions), 0)
    
    def test_record_credit_transaction(self):
        """Test recording a credit (income) transaction"""
        txn = self.cash_book.record_transaction(500, 'credit', 'Salary')
        self.assertEqual(txn['amount'], 500)
        self.assertEqual(txn['type'], 'credit')
        self.assertEqual(self.cash_book.current_balance, 1500)
        self.assertEqual(len(self.cash_book.transactions), 1)
    
    def test_record_debit_transaction(self):
        """Test recording a debit (expense) transaction"""
        txn = self.cash_book.record_transaction(200, 'debit', 'Groceries')
        self.assertEqual(txn['amount'], 200)
        self.assertEqual(txn['type'], 'debit')
        self.assertEqual(self.cash_book.current_balance, 800)
        self.assertEqual(len(self.cash_book.transactions), 1)
    
    def test_get_balance(self):
        """Test get_balance method"""
        self.assertEqual(self.cash_book.get_balance(), 1000)
        self.cash_book.record_transaction(500, 'credit', 'Income')
        self.assertEqual(self.cash_book.get_balance(), 1500)
    
    def test_get_total_credits(self):
        """Test get_total_credits method"""
        self.cash_book.record_transaction(500, 'credit', 'Income 1')
        self.cash_book.record_transaction(300, 'credit', 'Income 2')
        self.cash_book.record_transaction(100, 'debit', 'Expense')
        self.assertEqual(self.cash_book.get_total_credits(), 800)
    
    def test_get_total_debits(self):
        """Test get_total_debits method"""
        self.cash_book.record_transaction(200, 'debit', 'Expense 1')
        self.cash_book.record_transaction(150, 'debit', 'Expense 2')
        self.cash_book.record_transaction(300, 'credit', 'Income')
        self.assertEqual(self.cash_book.get_total_debits(), 350)
    
    def test_insufficient_balance(self):
        """Test that debit with insufficient balance raises error"""
        with self.assertRaises(ValueError):
            self.cash_book.record_transaction(2000, 'debit', 'Large expense')
    
    def test_negative_amount(self):
        """Test that negative amount raises error"""
        with self.assertRaises(ValueError):
            self.cash_book.record_transaction(-100, 'credit', 'Negative')
    
    def test_invalid_transaction_type(self):
        """Test that invalid transaction type raises error"""
        with self.assertRaises(ValueError):
            self.cash_book.record_transaction(100, 'invalid', 'Bad type')
    
    def test_invalid_date_format(self):
        """Test that invalid date format raises error"""
        with self.assertRaises(ValueError):
            self.cash_book.record_transaction(100, 'credit', 'Bad date', '05/19/2026')
    
    def test_get_transactions_all(self):
        """Test get_transactions without filters"""
        self.cash_book.record_transaction(500, 'credit', 'Income', '2026-05-01')
        self.cash_book.record_transaction(200, 'debit', 'Expense', '2026-05-02')
        
        transactions = self.cash_book.get_transactions()
        self.assertEqual(len(transactions), 2)
    
    def test_get_transactions_date_range(self):
        """Test get_transactions with date range"""
        self.cash_book.record_transaction(500, 'credit', 'Income 1', '2026-05-01')
        self.cash_book.record_transaction(200, 'debit', 'Expense 1', '2026-05-05')
        self.cash_book.record_transaction(300, 'credit', 'Income 2', '2026-05-10')
        
        transactions = self.cash_book.get_transactions(
            start_date='2026-05-04',
            end_date='2026-05-08'
        )
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['description'], 'Expense 1')
    
    def test_get_summary(self):
        """Test get_summary method"""
        self.cash_book.record_transaction(500, 'credit', 'Income')
        self.cash_book.record_transaction(200, 'debit', 'Expense')
        
        summary = self.cash_book.get_summary()
        self.assertEqual(summary['initial_balance'], 1000)
        self.assertEqual(summary['current_balance'], 1300)
        self.assertEqual(summary['total_credits'], 500)
        self.assertEqual(summary['total_debits'], 200)
        self.assertEqual(summary['transaction_count'], 2)
        self.assertEqual(summary['net_change'], 300)
    
    def test_transaction_id_assignment(self):
        """Test that transaction IDs are assigned correctly"""
        txn1 = self.cash_book.record_transaction(100, 'credit', 'Income 1')
        txn2 = self.cash_book.record_transaction(50, 'debit', 'Expense 1')
        txn3 = self.cash_book.record_transaction(200, 'credit', 'Income 2')
        
        self.assertEqual(txn1['id'], 1)
        self.assertEqual(txn2['id'], 2)
        self.assertEqual(txn3['id'], 3)
    
    def test_balance_after_tracking(self):
        """Test that balance_after is tracked correctly"""
        txn1 = self.cash_book.record_transaction(500, 'credit', 'Income')
        self.assertEqual(txn1['balance_after'], 1500)
        
        txn2 = self.cash_book.record_transaction(200, 'debit', 'Expense')
        self.assertEqual(txn2['balance_after'], 1300)
    
    def test_save_and_load_json(self):
        """Test saving and loading from JSON"""
        # Record some transactions
        self.cash_book.record_transaction(500, 'credit', 'Income')
        self.cash_book.record_transaction(200, 'debit', 'Expense')
        
        # Save to file
        filename = 'test_cash_book.json'
        self.cash_book.save_to_json(filename)
        
        # Load from file
        new_book = CashBook()
        new_book.load_from_json(filename)
        
        # Verify data matches
        self.assertEqual(new_book.initial_balance, self.cash_book.initial_balance)
        self.assertEqual(new_book.current_balance, self.cash_book.current_balance)
        self.assertEqual(len(new_book.transactions), len(self.cash_book.transactions))
        
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)
    
    def test_generate_report(self):
        """Test that generate_report returns a string"""
        self.cash_book.record_transaction(500, 'credit', 'Income')
        self.cash_book.record_transaction(200, 'debit', 'Expense')
        
        report = self.cash_book.generate_report()
        self.assertIsInstance(report, str)
        self.assertIn('CASH BOOK REPORT', report)
        self.assertIn('Income', report)
        self.assertIn('Expense', report)
    
    def test_multiple_transactions_balance(self):
        """Test balance calculation with multiple transactions"""
        self.assertEqual(self.cash_book.current_balance, 1000)
        
        self.cash_book.record_transaction(500, 'credit', 'Income 1')
        self.assertEqual(self.cash_book.current_balance, 1500)
        
        self.cash_book.record_transaction(300, 'debit', 'Expense 1')
        self.assertEqual(self.cash_book.current_balance, 1200)
        
        self.cash_book.record_transaction(200, 'credit', 'Income 2')
        self.assertEqual(self.cash_book.current_balance, 1400)
        
        self.cash_book.record_transaction(100, 'debit', 'Expense 2')
        self.assertEqual(self.cash_book.current_balance, 1300)


class TestCashBookEdgeCases(unittest.TestCase):
    """Test edge cases for CashBook class"""
    
    def test_zero_initial_balance(self):
        """Test CashBook with zero initial balance"""
        cash_book = CashBook(initial_balance=0)
        self.assertEqual(cash_book.get_balance(), 0)
        
        cash_book.record_transaction(100, 'credit', 'Income')
        self.assertEqual(cash_book.get_balance(), 100)
    
    def test_large_numbers(self):
        """Test CashBook with large numbers"""
        cash_book = CashBook(initial_balance=1000000)
        cash_book.record_transaction(500000, 'credit', 'Large income')
        self.assertEqual(cash_book.get_balance(), 1500000)
    
    def test_small_amounts(self):
        """Test CashBook with small decimal amounts"""
        cash_book = CashBook(initial_balance=100)
        cash_book.record_transaction(0.50, 'debit', 'Small expense')
        self.assertAlmostEqual(cash_book.get_balance(), 99.50, places=2)
    
    def test_many_transactions(self):
        """Test CashBook with many transactions"""
        cash_book = CashBook(initial_balance=1000)
        
        # Record 100 transactions
        for i in range(100):
            amount = (i + 1) * 10
            trans_type = 'credit' if i % 2 == 0 else 'debit'
            cash_book.record_transaction(amount, trans_type, f'Transaction {i+1}')
        
        self.assertEqual(len(cash_book.transactions), 100)


if __name__ == '__main__':
    unittest.main()
