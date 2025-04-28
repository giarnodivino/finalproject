from django.shortcuts import render
from .models import Employee, Payslip

# Create your views here.
def home(request):
    employee = Employee.objects.all()
    return render(request, 'payroll_app/home.html', {'employee':employee})