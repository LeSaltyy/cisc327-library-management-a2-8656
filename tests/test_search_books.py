import pytest
from library_service import search_books_in_catalog, add_book_to_catalog

def setup_module(module):
    add_book_to_catalog("Searchable Book", "AuthorX", "4444444444444", 1)

def test_search_by_title():
    results = search_books_in_catalog("searchable", "title")
    assert len(results) >= 1

def test_search_by_author():
    results = search_books_in_catalog("authorx", "author")
    assert len(results) >= 1

def test_search_by_isbn():
    results = search_books_in_catalog("4444444444444", "isbn")
    assert len(results) == 1

def test_search_invalid_term():
    results = search_books_in_catalog("", "title")
    assert results == []

def test_search_invalid_type():
    results = search_books_in_catalog("searchable", "publisher")
    assert results == []

# AI GENERATED TESTS 

def test_search_case_insensitive_title():
    results_lower = search_books_in_catalog("searchable book", "title")
    results_upper = search_books_in_catalog("SEARCHABLE BOOK", "title")
    assert len(results_lower) >= 1
    assert len(results_upper) >= 1

def test_search_partial_match_title():
    results = search_books_in_catalog("Book", "title")
    assert len(results) >= 2  # "Searchable Book" and "Another Book"

def test_search_partial_match_author():
    results = search_books_in_catalog("Author", "author")
    assert len(results) >= 3  # Matches all authors containing "Author"

def test_search_exact_isbn_only():
    results = search_books_in_catalog("5555555555555", "isbn")
    assert len(results) == 1
    assert results[0]["isbn"] == "5555555555555"

def test_search_nonexistent_title():
    results = search_books_in_catalog("Nonexistent Book", "title")
    assert results == []

def test_search_nonexistent_author():
    results = search_books_in_catalog("Ghost Author", "author")
    assert results == []

def test_search_numeric_in_title():
    add_book_to_catalog("Book 101", "AuthorZ", "7777777777777", 1)
    results = search_books_in_catalog("101", "title")
    assert len(results) == 1
    assert results[0]["title"] == "Book 101"

def test_search_multiple_keywords_in_title():
    add_book_to_catalog("Python Programming 101", "AuthorZ", "8888888888888", 1)
    results = search_books_in_catalog("Python 101", "title")
    assert len(results) >= 1
    titles = [book["title"] for book in results]
    assert any("Python Programming 101" in t for t in titles)