from django.urls import path
from . import views

urlpatterns = [
    path('producer/', views.producer_view, name='producer'),
    path('consumer/', views.consumer_view, name='consumer'),
]