from django.contrib import admin
from django.urls import path
from .views.account import Signin
from .views.book import BookView
from .views.author import AuthorView
from .views.review import ReviewView

urlpatterns = [
    path('signin/',Signin.as_view(),name='signin'),
    # book
    path('book-create/',BookView.as_view({'post':'create'}),name='book_create'),
    path('book-list/',BookView.as_view({'get':'list'}),name='book_lists'),
    # author
    path('author-create/',AuthorView.as_view({'post':'create'}),name='author_create'),
    path('author-list/',AuthorView.as_view({'get':'list'}),name='author_lists'),
    path('assign-book/<int:pk>/',AuthorView.as_view({'post':'assign_book'}),name='assign_book'),
    # review
    path('review/',ReviewView.as_view({'post':'create'}),name='review_create')
]
