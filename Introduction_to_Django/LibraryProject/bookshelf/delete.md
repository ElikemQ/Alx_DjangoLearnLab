python manage.py shell

from bookshelf.models import Book 

from yourapp.models import Book

new_book = Book.objects.get(title="Nineteen Eighty-Four", author="George Orwell")

new_book.delete()

all_books = Book.objects.all()
print(all_books)

Expected results 
<QuerySet []>