# Query all books by a specific author
from relationship_app.models import Author, Book
author = Author.objects.get(name="name_of_author")
books_by_author = Book.objects.filter(author=author)

for book in books_by_author:
    print(book.title)


# List all books in a library
from relationship_app.models import Library
books_in_library = Library.books.all()

for book in books_in_library:
    print(book.title)


from relationship_app.models import Library, Librarian
librarian = Librarian.objects.get(name="library_name")
print(librarian.name)