from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookSerializer
from .models import Book

class HealthView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "status": "ok"
        })

health_view = HealthView.as_view()

class BooksView(APIView):
    """ List all books, or create a new book """

    def get(self, request, *args, **kwargs):
        all_books = Book.objects.all()
        serializer = BookSerializer(all_books, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
books_view = BooksView.as_view()

class BookView(APIView):
    """ List, update or delete a book """

    def get(self, request, pk, *args, **kwargs):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, many=False)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response({
                'message': 'Book deleted successfully',
                }, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({
                "error": "Book not found"
            }, status=status.HTTP_404_NOT_FOUND)
 
book_view = BookView.as_view()