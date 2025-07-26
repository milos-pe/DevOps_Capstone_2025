from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Book
from datetime import date

### Test /api/books/ ###
class BooksViewTest(APITestCase):
    def test_get(self):
        book = Book.objects.create(
            title="Demo",
            description="Description",
            author="Author",
            isbn="1234567890123",
            published_date=date.today()
            )

        url = reverse('api:books')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body == [
            {
                'title': book.title,
                'description' : book.description,
                'author': book.author,
                'isbn': book.isbn,
                'published_date': book.published_date.isoformat(),
                'created_at': book.created_at.isoformat().replace("+00:00", "Z"),
            }
        ]

class BooksCreateTest(APITestCase):
    def test_create(self):
        data = {
            "title": "Demo",
            "description": "Description",
            "author": "Author",
            "isbn": "1234567890123",
            "published_date": date.today()
            }
        
        initial_count = Book.objects.count()
        
        url = reverse('api:books')
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert Book.objects.count() == initial_count + 1
    
    def test_create_fail(self):
        data = {
            "title": "",
            "description": "Description",
            "author": "Author",
            "isbn": "1234567890123",
            "published_date": date.today()
            }
        
        url = reverse('api:books')
        response = self.client.post(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

### Test /api/books/<id>/ ###
class BookViewTest(APITestCase):
    def test_get_book(self):
        book = Book.objects.create(
            title="Demo",
            description="Description",
            author="Author",
            isbn="1234567890123",
            published_date=date.today()
            )

        url = reverse('api:book', args=[book.pk])
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body == {
                'title': book.title,
                'description' : book.description,
                'author': book.author,
                'isbn': book.isbn,
                'published_date': book.published_date.isoformat(),
                'created_at': book.created_at.isoformat().replace("+00:00", "Z")
        }

class BookUpdateTest(APITestCase):
    def test_update_book(self):
        book = Book.objects.create(
            title="Demo",
            description="Description",
            author="Author",
            isbn="1234567890123",
            published_date=date.today()
            )
        
        data = {
            "title": "Demo v2",
            "description": "Description",
            "author": "Author",
            "isbn": "1234567890123",
            "published_date": date.today()
            }

        url = reverse('api:book', args=[book.pk])
        response = self.client.put(url, data, format="json")
        assert response.status_code == status.HTTP_202_ACCEPTED
        book.refresh_from_db()
        assert book.title == "Demo v2"

    def test_update_fail(self):
        book = Book.objects.create(
            title="Demo",
            description="Description",
            author="Author",
            isbn="1234567890123",
            published_date=date.today()
            )
        
        data = {
            "title": "Demo",
            "description": "Description",
            "author": "Author",
            "isbn": "1234567890123",
            }
        
        url = reverse('api:book', args=[book.pk])
        response = self.client.put(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        book.refresh_from_db()
        assert book.title == "Demo"

class BookDeleteTest(APITestCase):
    def test_delete_book(self):
        book = Book.objects.create(
            title="Demo",
            description="Description",
            author="Author",
            isbn="1234567890123",
            published_date=date.today()
            )

        initial_count = Book.objects.count()

        url = reverse('api:book', args=[book.pk])
        response = self.client.delete(url, format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Book.objects.count() == initial_count - 1

    def test_delete_fail(self):
            book = Book.objects.create(
            title="Demo",
            description="Description",
            author="Author",
            isbn="1234567890123",
            published_date=date.today()
            )

            id_test = 9999999

            url = reverse('api:book', args=[id_test])
            response = self.client.delete(url, format="json")
            assert response.status_code == status.HTTP_404_NOT_FOUND

### Test api:health ###
class HealthViewTest(APITestCase):
    def test_response_is_correct(self):
        url = reverse('api:health')
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["status"] == "ok"