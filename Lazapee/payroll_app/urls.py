from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('create_employee', views.create_employee, name='create_employee'),
    path('update_employee/<int:pk>/', views.update_employee, name='update_employee'),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('payslips/', views.payslips, name='payslips'),
    path('create_payslip/', views.create_payslip, name='create_payslip'),
]
