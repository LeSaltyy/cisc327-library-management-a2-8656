import pytest
import sys
from services.library_service import add_book_to_catalog

from database import reset_database  

@pytest.fixture(autouse=True)
def clear_db():
    reset_database()

def test_valid_input():
    success, message = add_book_to_catalog("Test Book", "Test Author", "1231107890121", 5)
    assert success is True
    #assert "successfully added" in message.lower()

def test_too_short():
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    assert success is False
    assert "ISBN must be exactly 13 digits." in message

def test_missing_title():
    success, message = add_book_to_catalog("", "Author", "1234567890123", 5)
    assert success is False
    assert "title is required" in message.lower()

def test_negative_copies():
    success, message = add_book_to_catalog("Test Book", "Author", "1234567890123", -2)
    assert success is False
    assert "total copies must be a positive integer" in message.lower()

def test_duplicate_isbn():
    add_book_to_catalog("Book1", "Author1", "1234567890123", 5)
    success, message = add_book_to_catalog("Book2", "Author2", "1234567890123", 3)
    assert success is False
    assert "already exists" in message.lower()

# AI GENERATED TESTS 

def test_missing_author():
    success, message = add_book_to_catalog("Test Book", "", "1234567890123", 5)
    assert success is False
    assert "author is required" in message.lower()

def test_copies_zero():
    success, message = add_book_to_catalog("Test Book", "Author", "1234567890123", 0)
    assert success is False
    assert "total copies must be a positive integer" in message.lower()

def test_isbn_non_numeric():
    success, message = add_book_to_catalog("Test Book", "Author", "ABCDEFGHIJKLM", 5)
    assert success is False
    assert "ISBN must be exactly 13 digits" in message

def test_whitespace_title_author():
    success, message = add_book_to_catalog("   ", "  ", "1234567890123", 5)
    assert success is False
    assert "title is required" in message.lower() or "author is required" in message.lower()

def test_large_number_of_copies():
    success, message = add_book_to_catalog("Big Book", "Author", "9876543210123", 1000)
    assert success is True
    # Ensure system can handle large but valid number of copies

def test_isbn_with_leading_zeros():
    success, message = add_book_to_catalog("Zero Book", "Author", "0000000000123", 5)
    assert success is True
    # Checks if ISBNs starting with zeros are handled correctly
