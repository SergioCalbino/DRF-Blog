from comments.api.views import CommentListApiView,CommentCreateApiView, CommentUpdateApiView
from django.urls import path

urlpatterns = [
    path('comments', CommentListApiView.as_view()),
    path('comments/create', CommentCreateApiView.as_view()),
    path('comments/<pk>', CommentUpdateApiView.as_view())
]