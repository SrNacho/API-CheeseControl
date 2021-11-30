from django.urls import path
from v1 import views

urlpatterns = [
    path('leche/', views.Leche.as_view(), name="leche"),
]
