python manage.py shell

from bookshelf.models import Book 
new_book = Book.objects.all()

print(new_book.__dict__)


Expected output
title: 1984
author: George Orwell
publication_year: 1949
print(f"Title: {book.title}")