import pytest
import assignment

def test_book():
    book = assignment.Book("1984", "George Orwell")
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.is_checked_out is False
    
    assert book.checkout() is True
    assert book.is_checked_out is True
    assert book.checkout() is False
    
    assert book.return_book() is True
    assert book.is_checked_out is False
    assert book.return_book() is False

def test_library():
    lib = assignment.Library()
    assert hasattr(lib, 'books')
    assert len(lib.books) == 0
    
    book1 = assignment.Book("1984", "George Orwell")
    book2 = assignment.Book("To Kill a Mockingbird", "Harper Lee")
    
    lib.add_book(book1)
    lib.add_book(book2)
    assert len(lib.books) == 2
    
    available = lib.get_available_books()
    assert len(available) == 2
    assert "1984" in available
    assert "To Kill a Mockingbird" in available
    
    book1.checkout()
    available = lib.get_available_books()
    assert len(available) == 1
    assert "To Kill a Mockingbird" in available
    assert "1984" not in available
