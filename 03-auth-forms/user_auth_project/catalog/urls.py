from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('preferences/', views.preferences, name='preferences'),
    path('session-summary/', views.session_summary, name='session_summary'),
]
