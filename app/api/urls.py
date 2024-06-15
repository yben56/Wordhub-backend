from django.urls import path
from . import views
from users.middleware import AuthenticationMiddleware

urlpatterns = [
    #Guest & User
    path('associate/<str:word>/', AuthenticationMiddleware(views.associate, optional=True)),
    path('quiz', AuthenticationMiddleware(views.quiz, optional=True)),
    path('search/<str:text>/', AuthenticationMiddleware(views.search, optional=True)),
    path('word/<str:word>/<int:wordid>/', AuthenticationMiddleware(views.word, optional=True)),
    path('words', AuthenticationMiddleware(views.words, optional=True)),

    #User Only
    path('answer', AuthenticationMiddleware(views.answer, optional=False)),
    path('history', AuthenticationMiddleware(views.history, optional=False)),
]