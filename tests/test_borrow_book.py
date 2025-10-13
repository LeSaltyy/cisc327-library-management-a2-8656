import pytest
from library_service import borrow_book_by_patron, add_book_to_catalog

def setup_module(module):
    # Ensure a test book exists
    add_book_to_catalog("Borrowable Book", "Author", "1111111111111", 2)

def test_valid():
    success, message = borrow_book_by_patron("123456", 1)
    assert success is True
    assert "successfully borrowed" in message.lower()

def test_invalid_patron():
    success, message = borrow_book_by_patron("abc123", 1)
    assert success is False
    assert "invalid patron id" in message.lower()

def test_unavailable():
    borrow_book_by_patron("123457", 1)  
    borrow_book_by_patron("654321", 1)  
    borrow_book_by_patron("624321", 1)  
    borrow_book_by_patron("634321", 1)  
    success, message = borrow_book_by_patron("111111", 1)
    assert success is False
    assert "currently not available" in message.lower()

def test_invalid_book_id():
    success, message = borrow_book_by_patron("123456", 999)
    assert success is False
    assert "book not found" in message.lower()

# AI GENERATED TESTS 

def test_negative_book_id():
    success, message = borrow_book_by_patron("123456", -1)
    assert success is False
    assert "book not found" in message.lower()

def test_zero_book_id():
    success, message = borrow_book_by_patron("123456", 0)
    assert success is False
    assert "book not found" in message.lower()

def test_whitespace_patron_id():
    success, message = borrow_book_by_patron("   ", 1)
    assert success is False
    assert "invalid patron id" in message.lower()

def test_multiple_borrows_same_patron():
    # First borrow succeeds
    success1, message1 = borrow_book_by_patron("123456", 2)
    assert success1 is True
    assert "successfully borrowed" in message1.lower()

    # Second borrow fails because patron already has it
    success2, message2 = borrow_book_by_patron("123456", 2)
    assert success2 is False
    assert "already borrowed" in message2.lower()

def test_borrow_after_return():
    # Borrow a book, simulate return, then borrow again
    borrow_book_by_patron("123456", 1)
    # Assume return_book_by_patron exists
    from library_service import return_book_by_patron
    return_book_by_patron("123456", 1)
    success, message = borrow_book_by_patron("123456", 1)
    assert success is True
    assert "successfully borrowed" in message.lower()
