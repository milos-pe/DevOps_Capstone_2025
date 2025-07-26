from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
