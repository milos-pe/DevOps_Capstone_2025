from django.urls import path
from .views import books_view, book_view, health_view

app_name = 'api'

urlpatterns = [
    path("health", health_view, name='health'),
    path("books/", books_view, name='books'),
    path("book/<int:pk>/", book_view, name='book')
	]