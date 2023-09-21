from django.contrib import admin
from django.urls import path, include
from .views import UserProductView, UserProductDetailView

urlpatterns = [
    path('<int:user_id>/products/', UserProductView.as_view()),
    path('<int:user_id>/products/<int:product_id>/', UserProductDetailView.as_view()),
    #path('statistics/', NotImplemented),
]