from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get-response/', views.get_response, name='get_response'),  # ✅ this is the endpoint
    path('clear-history/', views.clear_history, name='clear_history'),
]
