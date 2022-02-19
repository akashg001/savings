from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from .models import Addmoney_info,userprofile
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse
import datetime
from django.utils import timezone
import csv


def home(request):
    if request.session.has_key('is_logged'):
        return redirect('/index')
    return render(request,'home/login.html')
   # return HttpResponse('This is home')

def signup(request):
    return render(request,'home/login.html')
def index(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        money=Addmoney_info.objects.filter(user=user)
        exp = 0
        for i in money:
            if i.add_money == 'Expense':
                exp=exp+i.quantity
        money.exp=exp
        inc=0
        for i in money:
            if i.add_money == 'Income':
                inc=inc+i.quantity
        money.inc=inc
        bal=money.inc-money.exp
        money.bal=bal
        paginator = Paginator(addmoney_info , 5)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)

        context = {
           'page_obj' : page_obj,
           'money' : money
        }

        return render(request,'home/index.html',context)
    return redirect('home')
    #return HttpResponse('This is blog')
def register(request):
    return render(request,'home/register.html')
    #return HttpResponse('This is blog')
def password(request):
    return render(request,'home/password.html')

def profile_edit(request,id):
    if request.session.has_key('is_logged'):
        add = User.objects.get(id=id)
        return render(request,'home/profile_edit.html',{'add':add})
    return redirect("/home")

def profile_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user = User.objects.get(id=id)
            user.first_name = request.POST["fname"]
            user.email = request.POST["email"]
            user.save()
            return redirect("/profile")
    return redirect("/home")   


# Create your views here.
def handleSignup(request):
    if request.method =='POST':
            # get the post parameters
            uname = request.POST["uname"]
            fname=request.POST["fname"]
            email = request.POST["email"]
            pass1 = request.POST["pass1"]
            profile = userprofile()
            # check for errors in input
            if request.method == 'POST':
                try:
                    user_exists = User.objects.get(username=request.POST['uname'])
                    messages.error(request," Username already taken, Try something else!!!")
                    return redirect("/")    
                except User.DoesNotExist:
                    if len(uname)>15:
                        messages.error(request," Username must be max 15 characters, Please try again")
                        return redirect("/")
            
                    if not uname.isalnum():
                        messages.error(request," Username should only contain letters and numbers, Please try again")
                        return redirect("/")
            
                    
            # create the user
            user = User.objects.create_user(uname, email, pass1)
            user.first_name=fname
            user.email = email
            user.save()

            profile.user = user
            profile.save()
            messages.success(request," Your account has been successfully created")
            return redirect("/")
    else:
        return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def handlelogin(request):
    if request.method =='POST':
        # get the post parameters
        loginuname = request.POST["loginuname"]
        loginpassword1=request.POST["loginpassword1"]
        user = authenticate(username=loginuname, password=loginpassword1)
        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            user = request.user.id 
            request.session["user_id"] = user
            return redirect('/index')
        else:
            messages.error(request," Invalid Credentials, Please try again")  
            return redirect("/")  
    return HttpResponse('404-not found')

def handlelogout(request):
        del request.session['is_logged']
        del request.session["user_id"] 
        logout(request)
        messages.success(request, " Successfully logged out")
        return redirect('home')

#add money form

def addmoney(request):
    return render(request,'home/addmoney.html')
    
def addmoney_submission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            addmoney_info1 = Addmoney_info.objects.filter(user=user1).order_by('-Date')
            add_money = request.POST["add_money"]
            quantity = request.POST["quantity"]
            Date = request.POST["Date"]
            Category = request.POST["Category"]
            add = Addmoney_info(user = user1,add_money=add_money,quantity=quantity,Date = Date,Category= Category)
            add.save()
            return redirect(home)
    return redirect('/index')

def addmoney_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            add  = Addmoney_info.objects.get(id=id)
            add .add_money = request.POST["add_money"]
            add.quantity = request.POST["quantity"]
            add.Date = request.POST["Date"]
            add.Category = request.POST["Category"]
            add .save()
            return redirect("/index")
    return redirect("/home")        

def expense_edit(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        return render(request,'home/expense_edit.html',{'addmoney_info':addmoney_info})
    return redirect("/home")  

def expense_delete(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        addmoney_info.delete()
        return redirect("/index")
    return redirect("/home")  

def profile(request):
    if request.session.has_key('is_logged'):
        return render(request,'home/profile.html')
    return redirect('/home')

def export_csv(request):
    response=HttpResponse(content_type='text/csv')
    response['content_deposition']='attachment; Filename=Expenses'+'.csv'
    writer=csv.writer(response)
    writer.writerow(['Income/Expense','Amount','Date','Category'])
    expenses=Addmoney_info.objects.filter(user=request.user)
    for expense in expenses:
        writer.writerow([expense.add_money,expense.quantity,expense.Date,expense.Category])
    return response

def expense_category_sumary(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1)
    finalrep ={}
    def get_Category(addmoney_info):
        # if addmoney_info.add_money=="Expense":
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))
    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity
    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def income_category_sumary(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_income_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Income") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity
    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_income_category_amount(y,"Income")
    return JsonResponse({'income_category_data': finalrep}, safe=False)

def expense_category_weekly(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}
    def get_Category(addmoney_info):
        # if addmoney_info.add_money=="Expense":
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))
    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity
    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def income_category_weekly(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}
    def get_Category(addmoney_info):
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))
    def get_income_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Income") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity
    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_income_category_amount(y,"Income")
    return JsonResponse({'income_category_data': finalrep}, safe=False)

def expense_category_month(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=30)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        # if addmoney_info.add_money=="Expense":
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def income_category_month(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=30)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_income_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Income") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_income_category_amount(y,"Income")

    return JsonResponse({'income_category_data': finalrep}, safe=False)


def expense_category_half_year(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=30*6)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        # if addmoney_info.add_money=="Expense":
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def income_category_half_year(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=30*6)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_income_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Income") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_income_category_amount(y,"Income")

    return JsonResponse({'income_category_data': finalrep}, safe=False)


def expense_category_year(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=365)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        # if addmoney_info.add_money=="Expense":
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def income_category_year(request):
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=365)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_income_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Income") 
        for item in filtered_by_category:
            quantity+=item.quantity
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y]= get_income_category_amount(y,"Income")

    return JsonResponse({'income_category_data': finalrep}, safe=False)

def date_stats(request):
    return render(request,'home/date_stats.html')

def month_stats(request):
    return render(request,'home/month_stats.html')

def half_year_stats(request):
    return render(request,'home/half_year_stats.html')

def year_stats(request):
    return render(request,'home/year_stats.html')

def stats_view(request):
    return render(request,'home/stats.html')

def reports(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        addmoney = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney , 15)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {
           'page_obj' : page_obj,
           'addmoney':addmoney
        }
        return render(request,'home/report.html',context)
    return redirect('home')

def search(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        addmoney = Addmoney_info.objects.filter(user=user, Date__range=[fromdate,todate]).order_by('-Date')
        paginator = Paginator(addmoney , 15)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {
           'page_obj' : page_obj,
           'addmoney':addmoney
        }
        return render(request,'home/report.html',context)
    
    return redirect('home')
