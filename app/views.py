from django.shortcuts import render, redirect
from django.db import connection


# Create your views here.
def home(request):
    """Shows the product listing page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products ORDER BY productid")
        products = cursor.fetchall()

    result_dict = {'products': products}

    return render(request, 'app/home.html', result_dict)



# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request, 'app/view_admin.html', result_dict)

# Create your views here.
def register(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM allusers WHERE userid = %s", [request.POST['userid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['userid'], request.POST['phoneno'], request.POST['password'] ])
                return redirect('home')    
            else:
                status = 'User with ID %s already exists' % (request.POST['userid'])


    context['status'] = status
 
    return render(request, "app/register.html", context)

# Create your views here.
def login(request):
    """Shows the login page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM allusers WHERE userid = %s", [request.POST['userid']])
            user = cursor.fetchone()
            ## No customer with same id
            if user == None:
                cursor.execute("INSERT INTO allusers VALUES (%s, %s)"
                        , [request.POST['userid'], request.POST['password']])
                return redirect('home')
            else:
                status = 'Your User Id and Password is incorrect' % (request.POST['userid'])

    return render(request, 'app/login.html', context)

def profile(request, id):
    """Shows the main page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM allusers WHERE userid =  %s",[id])
        user = cursor.fetchone()

    result_dict = {'users': users}

    return render(request, 'app/profile.html', result_dict)


def view(request, productid):
    """Shows the main page"""

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE productid =  %s",[productid])
        products = cursor.fetchone()

    result_dict = {'products': products}

    return render(request, 'app/view.html', result_dict)
