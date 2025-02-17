python manage.py shell

from bookshelf.models import Book 

new_book = Book.objects.create (
    title = "1984",
    author = "George Orwell",
    publication_year = 1949)
new_book.save()

Expected Output 
new_book = Book(title="1984", author="George Orwell", publication_year=1949)