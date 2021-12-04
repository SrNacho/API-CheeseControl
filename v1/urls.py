from django.urls import path
from v1 import views

urlpatterns = [
    path('leche/', views.Leche.as_view(), name="leche"),
    path('curado/', views.Curado.as_view(), name="curado"),
    path('quesos/', views.Quesos.as_view(), name="quesos"),
]
