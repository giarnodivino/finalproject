from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip, Account
from django.contrib import messages


userid = None


def home(request):
    global userid

    if userid:
        employee = Employee.objects.all()
        return render(request, 'payroll_app/home.html', {'employee':employee})
    else:
        messages.error(request, f"Please Log in First")
        return redirect('login_page')

def add_overtime(request, pk):
    global userid
    if(request.method=="POST"):
        employee = get_object_or_404(Employee, pk=pk)
        overtime_hours = request.POST.get('othours')

        if overtime_hours:
            overtime_hours = float(overtime_hours) 
            employee.overtime_pay += (employee.rate/160 * 1.5 * overtime_hours)
            print(overtime_hours)
            employee.save() 

        return redirect('home')  
    else:
        return redirect('home')
    

def create_employee(request):
    global userid

    if userid:
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
    else:
        messages.error(request, f"Please Log in First")
        return redirect('login_page')
    
def update_employee(request, pk):
    global userid

    if userid:
        e = get_object_or_404(Employee, pk=pk)
        return render(request, 'payroll_app/update_employee.html', {"e":e})
    else:
        messages.error(request, f"Please Log in First")
        return redirect('login_page')

def delete_employee(request, pk):
    global userid
    e = get_object_or_404(Employee, pk=pk)
    Employee.objects.filter(pk=pk).delete()
    return redirect('home')


def payslips(request):
    global userid

    if userid:
        employee = Employee.objects.all()
        payslips = Payslip.objects.all().order_by('-year', '-month')
        return render(request, 'payroll_app/payslips.html', {'employee': employee, 'payslips': payslips})
    else:
        messages.error(request, f"Please Log in First")
        return redirect('login_page')

def create_payslip(request):
    global userid
    
    if(request.method=="POST"):
        payrollfor = request.POST.get('employee')
        month = request.POST.get('month')
        year = request.POST.get('year')
        cycle = int(request.POST.get('cycle'))


        if payrollfor == "all":
            employees = Employee.objects.all()
        else:
            employees = Employee.objects.filter(pk=payrollfor)

        for emp in employees:
            # Check if payslip already exists
            if Payslip.objects.filter(id_number=emp, month=month, year=year, pay_cycle=cycle).exists():
                messages.error(request, f"Payslip already exists for {emp.name} ({emp.id_number}) in {month} cycle {cycle}.")
                continue

            rate = emp.rate or 0
            allowance = emp.allowance or 0
            overtime = emp.overtime_pay or 0
            philhealth = 0
            sss = 0
            pag_ibig = 0

            if cycle == 1:
                pag_ibig = (100)
                tax = (rate/2 + allowance + overtime - pag_ibig)*0.2
                total_pay = (rate/2 + allowance + overtime -pag_ibig) - tax
            elif cycle == 2:
                philhealth = rate * 0.04
                sss = rate * 0.045
                tax = (rate/2 + allowance + overtime - philhealth - sss)*0.2
                total_pay = (rate/2 + allowance + overtime - philhealth - sss) - tax
            else:
                messages.error(request, f"Invalid cycle for {emp.name}.")
                continue


            Payslip.objects.create(
                id_number=emp,
                month=month,
                date_range="1-15" if cycle == 1 else "16-30",
                year=year,
                pay_cycle=cycle,
                rate=rate,
                earnings_allowance=allowance,
                deductions_tax=tax,
                deductions_health=philhealth,
                pag_ibig=pag_ibig,
                sss=sss,
                overtime=overtime,
                total_pay=total_pay,
            )

            # Reset overtime
            emp.overtime_pay = 0
            emp.save()

        return redirect('payslips')

    return redirect('payslips')


def login_page(request):
    global userid
    if(request.method=="POST"):
        uname = request.POST.get('uname')
        upass = request.POST.get('upass')
        account = Account.objects.filter(username=uname, password=upass).first()

        if account:
            userid = account.id
            print(userid)

            return redirect('home')
        else:
            messages.warning(request, "Incorrect Username or Password")
            return render(request, 'payroll_app/login_page.html')

    return render(request, 'payroll_app/login_page.html')

def signup_page(request):
    global userid

    if(request.method=="POST"):
        uname = request.POST.get('uname')
        upass = request.POST.get('upass')

        if not Account.objects.filter(username=uname).exists():
            Account.objects.create(username = uname, password = upass)
            messages.success(request, "Successfully Created Account")
            return redirect('login_page')
        else:
            messages.error(request, "Invalid: Account Already Exists")
            return render(request, 'payroll_app/signup_page.html')

    return render(request, 'payroll_app/signup_page.html')

def logout(request):
    global userid
    userid = None
    return redirect('login_page')