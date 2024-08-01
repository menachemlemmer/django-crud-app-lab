from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"book_id": self.id})

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    name = models.CharField(max_length=100)
    page = models.IntegerField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["page"]
