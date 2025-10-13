import pytest
from library_service import return_book_by_patron, borrow_book_by_patron, add_book_to_catalog

def setup_module(module):
    add_book_to_catalog("Returnable Book", "Author", "2222222222222", 2)
    borrow_book_by_patron("123456", 2)

def test_return_book_valid():
    success, message = return_book_by_patron("123456", 2)
    assert success is True
    assert "returned successfully" in message.lower()

def test_return_book_not_borrowed():
    success, message = return_book_by_patron("123456", 2)
    assert success is False
    assert "not currently borrowed" in message.lower()

def test_return_book_invalid_patron():
    success, message = return_book_by_patron("abc123", 2)
    assert success is False
    assert "invalid patron id" in message.lower()

def test_return_book_invalid_book():
    success, message = return_book_by_patron("123456", 999)
    assert success is False
    assert "book not found" in message.lower()

# AI GENERATED TESTS 

def test_return_book_twice():
    # Borrow a new book first
    add_book_to_catalog("Extra Book", "Author", "3333333333333", 1)
    borrow_book_by_patron("123456", 3)
    
    # Return it once
    success1, _ = return_book_by_patron("123456", 3)
    assert success1 is True

    # Try returning again
    success2, message2 = return_book_by_patron("123456", 3)
    assert success2 is False
    assert "not currently borrowed" in message2.lower()

def test_return_multiple_books():
    add_book_to_catalog("Book A", "Author", "4444444444444", 1)
    add_book_to_catalog("Book B", "Author", "5555555555555", 1)
    
    borrow_book_by_patron("123456", 4)
    borrow_book_by_patron("123456", 5)

    # Return both books
    success_a, _ = return_book_by_patron("123456", 4)
    success_b, _ = return_book_by_patron("123456", 5)

    assert success_a is True
    assert success_b is True

def test_return_book_empty_patron_id():
    success, message = return_book_by_patron("", 2)
    assert success is False
    assert "invalid patron id" in message.lower()

def test_return_book_none_patron_id():
    success, message = return_book_by_patron(None, 2)
    assert success is False
    assert "invalid patron id" in message.lower()

def test_return_book_not_in_catalog():
    success, message = return_book_by_patron("123456", 9999)
    assert success is False
    assert "book not found" in message.lower()

def test_return_book_by_one_of_multiple_patrons():
    # Add a new book and borrow by two patrons
    add_book_to_catalog("Shared Book", "Author", "6666666666666", 2)
    borrow_book_by_patron("123456", 6)
    borrow_book_by_patron("654321", 6)

    # Return book by first patron
    success, message = return_book_by_patron("123456", 6)
    assert success is True

    # Ensure second patron can still return
    success2, message2 = return_book_by_patron("654321", 6)
    assert success2 is True