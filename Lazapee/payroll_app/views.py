from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip
from django.contrib import messages

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

def payslips(request):
    employee = Employee.objects.all()
    payslips = Payslip.objects.all().order_by('-year', '-month')
    return render(request, 'payroll_app/payslips.html', {'employee': employee, 'payslips': payslips})

def create_payslip(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        month = request.POST.get('month')
        year = request.POST.get('year')
        cycle = int(request.POST.get('cycle'))

        if employee_id == "all":
            employee = Employee.objects.all()
        else:
            employee = employee = Employee.objects.filter(id_number=employee_id)

        for emp in employee:
            existing = Payslip.objects.filter(id_number=emp, month=month, year=year, pay_cycle=cycle)
            if existing.exists():
                messages.error(request, f"Payslip already exists for {emp.id_number} {month} Cycle {cycle}.")
                continue

            rate = emp.rate
            allowance = emp.allowance if emp.allowance else 0
            overtime_pay = emp.overtime_pay if emp.overtime_pay else 0

            if cycle == 1:
                pag_ibig = 100
                deductions_health = 0
                sss = 0
            else:
                pag_ibig = 0
                deductions_health = rate * 0.04
                sss = rate * 0.045

            cycle_rate = rate / 2
            tax = cycle_rate * 0.2
            total_pay = (cycle_rate + overtime_pay + allowance) - (tax + deductions_health + pag_ibig + sss)

            Payslip.objects.create(
                id_number=employee_id,
                month=month,
                date_range="1-15" if cycle == 1 else "16-30",
                year=year,
                pay_cycle=cycle,
                rate=rate,
                earnings_allowance=allowance,
                deductions_tax=tax,
                deductions_health=deductions_health,
                pag_ibig=pag_ibig,
                sss=sss,
                overtime=overtime_pay,
                total_pay=total_pay,
            )

            emp.overtime_pay = 0
            emp.save()

        return redirect('payslips')
    else:
        return redirect('payslips')