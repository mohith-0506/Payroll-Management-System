from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from .models import *
import datetime
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'payroll_manager/index.html')
def employee_dashboard(request,emp_id):
    user_info=user_paygrade=user_pay=user_achieve=user_leave=None
    user = Account.objects.get(user_id = emp_id)
    if user == request.user:
        if MEmployee.objects.filter(employee= user).exists():
            user_info = MEmployee.objects.get(employee= user)
        if MPaygrade.objects.filter(employee= user_info).exists():
            user_paygrade = MPaygrade.objects.filter(employee=user_info).first()
        if MPay.objects.filter(employee= user_info).exists():
            user_pay = MPay.objects.filter(employee=user_info).first()
        if TAchievement.objects.filter(employee= user_info).exists():
            user_achieve = TAchievement.objects.filter(employee=user_info)
        if TLeave.objects.filter(employee= user_info).exists():
            user_leave = TLeave.objects.filter(employee=user_info)
        return render(request,'payroll_manager/employee_dashboard.html', context={'user_info':user_info,'user_paygrade':user_paygrade,'user_pay':user_pay,'user_achieve':user_achieve,'user_leave':user_leave})
    else:
        messages.info(request, 'You Are Not Authorized To Access That Page')
        return redirect('index')
def employee_login(request):
    if request.method == 'POST':
        Acc = Account()
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(username = user_id , password = password )
        if user is not None:
            if Account.objects.filter(user_id=user_id, is_employee=True).exists():
                login(request,user)
                return redirect('employee_dashboard',emp_id=user_id)
            else:
                messages.info(request, 'Invalid, user not An Employee.')
                form = EmployeeLogin()
                return render(request,'payroll_manager/employee_login.html',context={'form':form})
        else:
            messages.info(request, 'Invalid Credentials.')
            form = EmployeeLogin()
            return render(request,'payroll_manager/employee_login.html',context={'form':form})
    form = EmployeeLogin()
    return render(request,'payroll_manager/employee_login.html',context={'form':form})

def admin_dashboard(request):
    if Account.objects.filter(user_id= request.user.user_id, is_employer=True):
        allEmp = MEmployee.objects.all()
        LeaveRequests = TLeave.objects.filter(is_approved=0)
        return render(request,'payroll_manager/admin_dashboard.html', context={'allEmp':allEmp, 'LeaveR':LeaveRequests})
    else:
        messages.info(request, 'You Are Not Authorized To Access That Page')
        return redirect('index')
def admin_login(request):
    if request.method == 'POST':
        Acc = Account()
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        user = authenticate(username = user_id , password = password )
        if user is not None:
            if Account.objects.filter(user_id=user_id, is_employer=True).exists():
                login(request,user)
                return redirect('admin_dashboard')
            else:
                messages.info(request, 'Invalid, user not An Admin.')
                form = EmployeeLogin()
                return render(request,'payroll_manager/admin_login.html',context={'form':form})
        else:
            messages.info(request, 'Invalid Credentials.')
            form = EmployeeLogin()
            return render(request,'payroll_manager/admin_login.html',context={'form':form})
    form = EmployeeLogin()
    return render(request,'payroll_manager/admin_login.html',context={'form':form})
def register(request):
    if request.method == 'POST':
        user = Account()
        if request.POST.get('password1') == request.POST.get('password2'):
            user.user_id = request.POST.get('user_id')
            user.set_password(request.POST.get('password1'))
            user.is_employee=True
            user.is_employer=False
            user.date_joined=datetime.datetime.now()
            user.save()
            add = MEmployee()

            add.employee = user
            add.employee_name = request.POST.get('employee_name')
            add.employee_doj = request.POST.get('employee_doj')
            add.department = MDepartment.objects.get(department_id=request.POST.get('department'))
            add.company = MCompany.objects.get(company_id=request.POST.get('company'))
            add.grade = MGrade.objects.get(grade_id=request.POST.get('grade'))
            add.save()
            return redirect('admin_dashboard')
    form = RegisterEmployeeForm()
    formSub = employeeInfoForm()
    return render(request,'payroll_manager/register.html',context={'form':form,'formSub':formSub})

def logoutUser(request):
    logout(request)
    return redirect('index')
def deleteAll(request):
    Account.objects.all().delete()
    return redirect('index')
def leaveApply(request,emp_id):
    user = Account.objects.get(user_id = emp_id)
    if user == request.user:
        if request.method == 'POST':
            leaveApp = TLeave()
            leaveApp.employee = MEmployee.objects.get(employee=user)
            leaveApp.fin_year= int(datetime.datetime.now().year)
            leaveApp.leave_date = request.POST.get('leave_date')
            leaveApp.leave_type=request.POST.get('leave_type')
            leaveApp.save()
            messages.success(request, 'Leave Application Submitted.')
            return redirect('employee_dashboard', emp_id=emp_id)
        leaveForm = leaveApplyForm()
        return render(request,'payroll_manager/leaveApply.html',context={'form':leaveForm})
def changeAddress(request,emp_id):
    user = Account.objects.get(user_id = emp_id)
    if True:
        if request.method == 'POST':
            if MAddress.objects.filter(memployee=MEmployee.objects.get(employee=user)).exists():
                add = MAddress.objects.filter(memployee=MEmployee.objects.get(employee=user)).first()
            else:
                add = MAddress()
                add.employee = MEmployee.objects.get(employee=user)
            add.building_details = request.POST.get('building_details')
            add.road = request.POST.get('road')
            add.landmark = request.POST.get('landmark')
            add.city = request.POST.get('city')
            add.state = MState.objects.get(state_code=request.POST.get('state')) 
            add.country = request.POST.get('country')
            add.save()
            messages.success(request, 'Address Details Updated.')
            if request.user.is_employer :
                return redirect('admin_dashboard')
            else: 
                return redirect('employee_dashboard', emp_id=emp_id)
        oldData = MAddress.objects.filter(memployee=MEmployee.objects.get(employee=user)).first()
        AddForm = addressForm(instance=oldData)
        return render(request,'payroll_manager/addressChange.html',context={'form':AddForm})
def admin_employee_dashboard(request,emp_id):
    if Account.objects.filter(user_id= request.user.user_id, is_employer=True):
        user_info=user_paygrade=user_pay=user_achieve=user_leave=None
        user = Account.objects.get(user_id = emp_id)
        # if request.user.is_admin:
        if MEmployee.objects.filter(employee= user).exists():
            user_info = MEmployee.objects.get(employee= user)
        if MPaygrade.objects.filter(employee= user_info).exists():
            user_paygrade = MPaygrade.objects.filter(employee=user_info).first()
            print(user_paygrade)
        if MPay.objects.filter(employee= user_info).exists():
            user_pay = MPay.objects.filter(employee=user_info).first()
        if TAchievement.objects.filter(employee= user_info).exists():
            user_achieve = TAchievement.objects.filter(employee=user_info)
        if TLeave.objects.filter(employee= user_info).exists():
            user_leave = TLeave.objects.filter(employee=user_info)
        return render(request,'payroll_manager/admin_employee_dashboard.html', context={'user_info':user_info,'user_paygrade':user_paygrade,'user_pay':user_pay,'user_achieve':user_achieve,'user_leave':user_leave})
    else:
        messages.info(request, 'You Are Not Authorized To Access That Page')
        return redirect('index')

def changePay(request,emp_id):
    user = Account.objects.get(user_id = emp_id)
    if True:
        if request.method == 'POST':
            if MPay.objects.filter(employee=MEmployee.objects.get(employee=user)).exists():
                addPay = MPay.objects.filter(employee=MEmployee.objects.get(employee=user)).first()
            else:
                addPay = MPay()
                addPay.employee = MEmployee.objects.get(employee=user)
            if MPaygrade.objects.filter(employee=MEmployee.objects.get(employee=user)).exists():
                addPaygrade = MPaygrade.objects.filter(employee=MEmployee.objects.get(employee=user)).first()
            else:
                addPaygrade = MPaygrade()
                addPaygrade.employee = MEmployee.objects.get(employee=user)
            addPay.employee = MEmployee.objects.get(employee=user)
            addPaygrade.employee = MEmployee.objects.get(employee=user)
            addPay.fin_year = int(datetime.datetime.now().year)
            addPay.gross_salary = request.POST.get('gross_salary')
            addPay.gross_dedn = request.POST.get('gross_dedn')
            addPay.net_salary = request.POST.get('net_salary')
            addPaygrade.grade = MEmployee.objects.get(employee=user).grade
            addPaygrade.basic_amt = request.POST.get('basic_amt')
            addPaygrade.da_amt = request.POST.get('da_amt')
            addPaygrade.pf_amt = request.POST.get('pf_amt')
            addPaygrade.medical_amt = request.POST.get('medical_amt')
            addPay.save()
            addPaygrade.save()
            messages.success(request, 'Income Details Updated.')
            return redirect('admin_dashboard')
        oldDataPay = MPay.objects.filter(employee=MEmployee.objects.get(employee=user)).first()
        oldDataPaygrade = MPaygrade.objects.filter(employee=MEmployee.objects.get(employee=user)).first()
        AddFormpay = payForm(instance=oldDataPay)
        AddFormpaygrade = paygradeForm(instance=oldDataPaygrade)
        return render(request,'payroll_manager/payChange.html',context={'formPay':AddFormpay,'formPaygrade':AddFormpaygrade})
def changeInfo(request,emp_id):
    user = Account.objects.get(user_id = emp_id)
    if True:
        if request.method == 'POST':
            if MEmployee.objects.filter(employee=user).exists():
                add = MEmployee.objects.get(employee=user)
            else:
                add = MEmployee()
                add.employee = user
            add.employee_name = request.POST.get('employee_name')
            add.employee_doj = request.POST.get('employee_doj')
            add.department = MDepartment.objects.get(department_id=request.POST.get('department'))
            add.company = MCompany.objects.get(company_id=request.POST.get('company'))
            add.grade = MGrade.objects.get(grade_id=request.POST.get('grade'))
            add.save()
            messages.success(request, 'Personal Details Updated.')
            return redirect('admin_dashboard')
        oldData = MEmployee.objects.get(employee=user)
        AddForm = employeeInfoForm(instance=oldData)
        return render(request,'payroll_manager/infoChange.html',context={'form':AddForm})
def changeAchievement(request,emp_id):
    user = Account.objects.get(user_id = emp_id)
    employee = MEmployee.objects.get(employee=user)
    if request.method == 'POST':
        achievement = TAchievement()
        achievement.employee = MEmployee.objects.get(employee=user)
        achievement.achievement_date = request.POST.get('achievement_date')
        achievement.achievement_type = request.POST.get('achievement_type')
        achievement.save()

        if MPay.objects.filter(employee=employee).exists():
            pay = MPay.objects.get(employee=employee)
            pay.achivement_reward += 500  # Increase gross salary by 500
            pay.net_salary = pay.gross_salary + pay.achivement_reward - pay.gross_dedn     # Increase net salary by 500 as well
            pay.save()
            messages.success(request, 'Achievement added and salary updated by 500.')

        return redirect('admin_dashboard')
    form = AchievementForm()
    return render(request,'payroll_manager/achievementChange.html',context={'form':form})

def update_salary_based_on_leave(user):
    total_leaves = TLeave.objects.filter(employee = MEmployee.objects.get(employee=user), is_approved=1).count()
    leave_rate = 100

    employee = MEmployee.objects.get(employee=user)
    if MPay.objects.filter(employee=employee).exists():
        pay = MPay.objects.get(employee=employee)
        gross_salary = pay.gross_salary
        pay.gross_dedn += leave_rate
        gross_deddn = pay.gross_dedn
        net_salary = gross_salary - gross_deddn
        pay.net_salary = net_salary
        pay.save()

def approval(request,leave_id,app_id):
    leave = TLeave.objects.get(leave_id=leave_id)
    if app_id == 1:
        leave.is_approved = 1
    else:
        leave.is_approved = -1
    leave.save()

    update_salary_based_on_leave(leave.employee.employee)

    return redirect('admin_dashboard')

def delete_employee(request, emp_id):
    if Account.objects.filter(user_id=request.user.user_id, is_employer=True).exists():
        try:
            user = Account.objects.get(user_id=emp_id)
            user.delete()
            messages.success(request, f"Employee with ID {emp_id} has been deleted successfully.")
        except Account.DoesNotExist:
            messages.error(request, f"Employee with ID {emp_id} does not exist.")
        return redirect('admin_dashboard')
    else:
        messages.error(request, "You are not authorized to delete employees.")
        return redirect('index')
    
def confirm_delete_employee(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        password = request.POST.get("password")
        print("Received emp_id:", emp_id)
        # Authenticate the current user with the entered password
        user = authenticate(username=request.user.user_id, password=password)
        
        if user is not None and user.is_employer:
            try:
                employee = Account.objects.get(user_id=emp_id)
                employee.delete()
                messages.success(request, f"Employee with ID {emp_id} has been deleted successfully.")
            except Account.DoesNotExist:
                messages.error(request, f"Employee with ID {emp_id} does not exist.")
        else:
            messages.error(request, "Password is incorrect or you do not have permission to delete employees.")
        
    return redirect('admin_dashboard')
