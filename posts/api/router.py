from rest_framework.routers import DefaultRouter
from posts.api.views import  PostListView, PostCreateView, PostDetailView
from django.urls import path



# router_posts = DefaultRouter()
# router_posts.register(prefix='posts', basename='posts', viewset=PostApiViewSet)

urlpatterns = [
    path('posts', PostListView.as_view() ),
    path('posts/create', PostCreateView.as_view()),
    path('posts/<slug>', PostDetailView.as_view())
]