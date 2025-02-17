python manage.py shell

from bookshelf.models import Book 
new_book = Book.objects.get(title="1984", author="George Orwell")
new_book.title = "Nineteen Eighty-Four"
new_book.save()

Expected results
print(new_book.title)
Nineteen Eighty-Four


