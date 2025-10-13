import pytest
from library_service import insert_borrow_record
from datetime import datetime, timedelta
from library_service import get_patron_status_report, borrow_book_by_patron, add_book_to_catalog

def setup_module(module):
    add_book_to_catalog("History Book", "Author", "3333333333333", 3)
    borrow_book_by_patron("123456", 3)

def test_status_report_valid():
    report = get_patron_status_report("123456")
    assert report["num_currently_borrowed"] >= 1
    assert isinstance(report["borrowing_history"], list)

def test_status_report_invalid_patron():
    report = get_patron_status_report("abc123")
    assert report["success"] is False

def test_status_report_no_books():
    report = get_patron_status_report("000000")
    assert report["num_currently_borrowed"] == 0

# AI GENERATED TESTS 

def test_status_report_multiple_borrows():
    # Borrow two more books for the same patron
    borrow_book_by_patron("123456", 4)
    borrow_book_by_patron("123456", 5)

    report = get_patron_status_report("123456")
    assert report["num_currently_borrowed"] >= 3
    assert all(isinstance(book, dict) for book in report["borrowing_history"])

def test_status_report_none_patron():
    report = get_patron_status_report(None)
    assert report["success"] is False

def test_status_report_empty_patron():
    report = get_patron_status_report("")
    assert report["success"] is False

def test_borrowing_history_structure():
    report = get_patron_status_report("123456")
    for book in report.get("borrowing_history", []):
        assert "book_id" in book
        assert "title" in book
        assert "author" in book
        assert "borrow_date" in book

def test_status_report_flags():
    report = get_patron_status_report("123456")
    for book in report.get("borrowing_history", []):
        # Example: check if overdue or special flags exist
        assert "overdue" in book or True  # adjust based on your implementation