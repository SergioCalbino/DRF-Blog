from rest_framework.routers import DefaultRouter
from categories.api.views import CategoryApiViewSet, CategoryCreateApiView, CategoryListApiView, CategoryDetailView
from django.urls import path



# router_categories = DefaultRouter()
#
# router_categories.register(prefix='categories', basename='categories', viewset=CategoryApiViewSet)

urlpatterns = [
    path('categories/create', CategoryCreateApiView.as_view()),
    path('categories/', CategoryListApiView.as_view()),
    path('categories/<slug>', CategoryDetailView.as_view())
]