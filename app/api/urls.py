from django.urls import path
from . import views
from users.middleware import AuthenticationMiddleware

urlpatterns = [
    path('words', AuthenticationMiddleware(views.words, optional=True)),
    path('search', AuthenticationMiddleware(views.search, optional=True)),
    path('word', AuthenticationMiddleware(views.word, optional=True)),
    path('quizs', AuthenticationMiddleware(views.quizs, optional=True)),
]