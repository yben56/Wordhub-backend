from django.urls import path
from . import views
from users.middleware import AuthenticationMiddleware

urlpatterns = [
    #Guest & User
    path('associate/<str:word>', AuthenticationMiddleware(views.associate, optional=True)),
    path('quiz', AuthenticationMiddleware(views.quiz, optional=True)),
    path('search/<str:text>', AuthenticationMiddleware(views.search, optional=True)),
    path('word/<str:word>/<int:wordid>', AuthenticationMiddleware(views.word, optional=True)),

    path('words', AuthenticationMiddleware(views.words, optional=True)),
    path('words/distribution', AuthenticationMiddleware(views.words_distribution, optional=False)),

    #User Only
    path('answer', AuthenticationMiddleware(views.answer, optional=False)),
    path('history', AuthenticationMiddleware(views.history, optional=False)),
    
    #Openedit GET, PUT
    path('openedit/word/<str:word>/<int:wordid>', AuthenticationMiddleware(views.openedit_word, optional=False)),
    path('openedit/quiz/<str:word>/<int:wordid>', AuthenticationMiddleware(views.openedit_quiz, optional=False)),
    #Openedit Post
    path('openedit/word', AuthenticationMiddleware(views.openedit_word, optional=False)),

    path('dictionarylist/<str:type>', views.dictionarylist),
]