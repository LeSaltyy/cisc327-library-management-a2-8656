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
    from database import get_book_by_isbn
    from library_service import add_book_to_catalog
    
    success, msg = add_book_to_catalog("Late Fee Test Book", "Test Author", "9999999999996", 1)
    assert success
    
    book = get_book_by_isbn("9999999999996")
    book_id = book['id']
    
    past_borrow = datetime.now() - timedelta(days=14)
    past_due = datetime.now() - timedelta(days=1)
    insert_borrow_record("123456", book_id, past_borrow, past_due)
    
    fee = calculate_late_fee_for_book("123456", book_id)
    assert fee["fee_amount"] > 0

def test_fee_seven_days_late():
    from database import get_book_by_isbn
    from library_service import add_book_to_catalog
    
    success, msg = add_book_to_catalog("Seven Days Late Book", "Test Author", "9999999999997", 1)
    assert success
    
    book = get_book_by_isbn("9999999999997")
    book_id = book['id']
    
    past_borrow = datetime.now() - timedelta(days=14)
    past_due = datetime.now() - timedelta(days=7)
    insert_borrow_record("123456", book_id, past_borrow, past_due)

    fee = calculate_late_fee_for_book("123456", book_id)
    assert fee["fee_amount"] == 3.5  # 7 days * $0.50

def test_fee_more_than_seven_days_under_max():
    from database import get_book_by_isbn
    from library_service import add_book_to_catalog
    
    success, msg = add_book_to_catalog("Eight Days Late Book", "Test Author", "9999999999998", 1)
    assert success
    
    book = get_book_by_isbn("9999999999998")
    book_id = book['id']
    
    past_borrow = datetime.now() - timedelta(days=10)
    past_due = datetime.now() - timedelta(days=8)
    insert_borrow_record("123456", book_id, past_borrow, past_due)

    fee = calculate_late_fee_for_book("123456", book_id)
    assert fee["fee_amount"] > 3.5  # Should be 7*0.50 + 1*1.00 = 4.50

def test_fee_exceeds_maximum():
    from database import get_book_by_isbn
    from library_service import add_book_to_catalog
    
    success, msg = add_book_to_catalog("Max Fee Book", "Test Author", "9999999999999", 1)
    assert success
    
    book = get_book_by_isbn("9999999999999")
    book_id = book['id']
    
    past_borrow = datetime.now() - timedelta(days=30)
    past_due = datetime.now() - timedelta(days=25)
    insert_borrow_record("123456", book_id, past_borrow, past_due)

    fee = calculate_late_fee_for_book("123456", book_id)
    assert fee["fee_amount"] == 15  # Capped at $15
