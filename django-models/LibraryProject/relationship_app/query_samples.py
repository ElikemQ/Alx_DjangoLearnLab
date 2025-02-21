# Query all books by a specific author
from relationship_app.models import Author, Book
author = Author.objects.get(name="name_of_author")
books_by_author = Book.objects.filter(author=author)

for book in books_by_author:
    print(book.title)


List all books in a library
from relationship_app.models import Library
library = Library.objects.get(name="library_name")

books_in_library = library.books.all()
for book in books_in_library:
    print(book.title)


from relationship_app.models import Library, Librarian
librarian = Librarian.objects.get(library="name_of_library")
print(librarian.name)