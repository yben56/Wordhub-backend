from django.urls import path
from . import views
from users.middleware import AuthenticationMiddleware

urlpatterns = [
    path('word/<str:word>/<int:wordid>/', AuthenticationMiddleware(views.word, optional=True)),
    path('words', AuthenticationMiddleware(views.words, optional=True)),
    path('quiz', AuthenticationMiddleware(views.quiz, optional=True)),
    path('search/<str:word>/', AuthenticationMiddleware(views.search, optional=True)),
]