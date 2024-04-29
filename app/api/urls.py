from django.urls import path
from . import views
from users.middleware import AuthenticationMiddleware, UserIdMiddleware

urlpatterns = [
    path('words', UserIdMiddleware(views.words)),
    path('search', UserIdMiddleware(views.search)),
    path('word', UserIdMiddleware(views.word)),
    path('quizs', UserIdMiddleware(views.quizs)),

    path('connectapi', views.connectapi),
    path('connectapi_lock', AuthenticationMiddleware(views.connectapi_lock)),
]