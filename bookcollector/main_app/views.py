from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .models import Book
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Book
from .forms import BookmarkForm


# Create your views here.


class Home(LoginView):
    template_name = "home.html"


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("book-index")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "signup.html", context)


@login_required
def book_index(request):
    books = Book.objects.filter(user=request.user)
    return render(request, "books/index.html", {"books": books})


@login_required
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    bookmark_form = BookmarkForm()
    return render(
        request, "books/detail.html", {"book": book, "bookmark_form": bookmark_form}
    )


@login_required
def add_bookmark(request, book_id):
    form = BookmarkForm(request.POST)
    if form.is_valid():
        new_bookmark = form.save(commit=False)
        new_bookmark.book_id = book_id
        new_bookmark.save()
    return redirect("book-detail", book_id=book_id)


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ["title", "author", "description", "year"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ["author", "description", "year"]


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = "/books/"
