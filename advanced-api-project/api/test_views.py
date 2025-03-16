from django.contrib.auth.models import User
from django.test import APITestCase
from rest_framework.test import APIClient 
from rest_framework import status
from .models import Book

class BookAPITest(APITestCase):
    def setUp(self):
        """Set up the test client and test data"""
        self.client.login(username='testuser', password='testpass')

        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.book = Book.objects.create(title="Test Book", author="John Doe", publication_year=2023)

    def test_list_books(self):
        """Test listing all books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", response.data[0]['title'])

    def test_create_book(self):
        """Test creating a book"""
        data = {"title": "New Book", "author": "Jane Doe", "publication_year": 2024}
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        """Test updating a book"""
        data = {"title": "Updated Title"}
        response = self.client.put(f'/api/books/{self.book.id}/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        """Test deleting a book"""
        response = self.client.delete(f'/api/book/{self.book.id}/delete')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books(self):
        """Test filtering books by author"""
        response = self.client.get('/api/books/?author=John Doe')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        """Test searching books by title"""
        response = self.client.get('/api/books/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books(self):
        """Test ordering books by publication_year"""
        Book.objects.create(title="Older Book", author="Jane Doe", publication_year=2020)
        response = self.client.get('/api/books/?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Older Book")