import pytest
from library_service import calculate_late_fee_for_book, borrow_book_by_patron, add_book_to_catalog, return_book_by_patron, insert_borrow_record
from datetime import timedelta, datetime

def setup_module(module):
    add_book_to_catalog("Late Fee Book", "AuthorY", "5555555555555", 1)
    borrow_book_by_patron("123456", 4)

def test_fee_not_overdue():
    fee = calculate_late_fee_for_book("123456", 4)
    assert fee["fee_amount"] == 0

def test_fee_book_not_borrowed():
    fee = calculate_late_fee_for_book("123456", 999)
    assert fee["fee_amount"] == 0
    assert fee["status"] == "Book not borrowed"

def test_fee_invalid_patron():
    fee = calculate_late_fee_for_book("abc123", 4)
    assert fee["fee_amount"] == 0

# AI GENERATED TESTS 

def test_fee_one_day_late():
    past_borrow = datetime.now() - timedelta(days=14)
    past_due = datetime.now() - timedelta(days=1)
    insert_borrow_record("123456", 6, past_borrow, past_due)
    
    fee = calculate_late_fee_for_book("123456", 6)
    assert fee["fee_amount"] > 0
    assert fee["fee_amount"] <= 7  # assuming $1/day for first 7 days

def test_fee_seven_days_late():
    past_borrow = datetime.now() - timedelta(days=14)
    past_due = datetime.now() - timedelta(days=7)
    insert_borrow_record("123456", 7, past_borrow, past_due)
    
    fee = calculate_late_fee_for_book("123456", 7)
    assert fee["fee_amount"] == 7  # assuming max $7 for 7 days

def test_fee_more_than_seven_days_under_max():
    past_borrow = datetime.now() - timedelta(days=10)
    past_due = datetime.now() - timedelta(days=8)
    insert_borrow_record("123456", 8, past_borrow, past_due)
    
    fee = calculate_late_fee_for_book("123456", 8)
    assert fee["fee_amount"] > 7  # additional $0.5/day after 7 days
    assert fee["fee_amount"] < 10  # should be under max fee

def test_fee_exceeds_maximum():
    past_borrow = datetime.now() - timedelta(days=30)
    past_due = datetime.now() - timedelta(days=25)
    insert_borrow_record("123456", 9, past_borrow, past_due)
    
    fee = calculate_late_fee_for_book("123456", 9)
    assert fee["fee_amount"] == 10  # assuming maximum late fee is $10

def test_fee_book_returned_late():
    past_borrow = datetime.now() - timedelta(days=10)
    past_due = datetime.now() - timedelta(days=5)
    insert_borrow_record("123456", 10, past_borrow, past_due)
    
    # Patron returns book
    return_book_by_patron("123456", 10)
    
    fee = calculate_late_fee_for_book("123456", 10)
    assert fee["fee_amount"] > 0
    assert fee["status"] == "Book returned late"