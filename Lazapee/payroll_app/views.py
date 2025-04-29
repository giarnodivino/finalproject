from django.shortcuts import render, redirect, get_object_or_404
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
        if not Employee.objects.filter(id_number=idnum).exists() and allowance:
            Employee.objects.create(name=name, id_number=idnum, rate=rate, allowance=allowance)
        elif not Employee.objects.filter(id_number=idnum).exists():
            Employee.objects.create(name=name, id_number=idnum, rate=rate)
        else:
            return redirect('create_employee')
        return redirect('home')
    else:
        employee = Employee.objects.all()
        return render(request, 'payroll_app/create_employee.html', {'employee':employee})
    
def update_employee(request, pk):
    e = get_object_or_404(Employee, pk=pk)
    return render(request, 'payroll_app/update_employee.html', {"e":e})

def delete_employee(request, pk):
    e = get_object_or_404(Employee, pk=pk)
    Employee.objects.filter(pk=pk).delete()
    return redirect('home')