from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('create_employee', views.create_employee, name='create_employee'),
    path('update_employee/<int:pk>/', views.update_employee, name='update_employee'),
]
