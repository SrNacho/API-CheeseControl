from django.urls import path
from v1 import views

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name="hello"),
]
