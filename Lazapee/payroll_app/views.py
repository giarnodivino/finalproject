from django.shortcuts import render, redirect
from .models import Employee, Payslip

# Create your views here.
def home(request):
    employee = Employee.objects.all()
    return render(request, 'payroll_app/home.html', {'employee':employee})

def create_employee(request):
    if(request.method=="POST"):
        name = request.POST.get('name')
        idnum = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        Employee.objects.create(name=name, id_number=idnum, rate=rate, allowance=allowance)
        return redirect('home')
    else:
        employee = Employee.objects.all()
        return render(request, 'payroll_app/create_employee.html', {'employee':employee})

