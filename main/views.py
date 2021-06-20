from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import stocklist, Query
from django.http import JsonResponse
from django.views.generic import View, TemplateView
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class MainView(TemplateView):
    template_name='index.html'

class PostJsonListView(View):
    def get(self, *args, **kwargs):
        # upper and lower are first and last stock name number that's going to load
        upper = kwargs.get('num_posts') #5
        lower = upper -5 #0
        stocks = list(stocklist.objects.values()[lower:upper])
        stock_size = len(stocklist.objects.all())
        max_size = True if upper >= stock_size else False
        return JsonResponse({'data': stocks, 'max': max_size}, safe=False)

def stockdetail(request, Sno):
    stock = stocklist.objects.get(Sno=Sno)
    return render(request, 'stockdetail.html', {'stock':stock})

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allstocks = stocklist.objects.none()
    else:
        allstockstitle = stocklist.objects.filter(title__contains=query)
        allstocksdesc = stocklist.objects.filter(desc__icontains=query)
        allstocks = allstockstitle.union(allstocksdesc)
    if allstocks.count() == 0:
        messages.warning(request, "No search results found. Please refine your query ")
    params = {'allstocks': allstocks, 'query':query}
    return render(request, 'search.html', params)

@csrf_exempt
def ask_query(request):
    if request.method == 'POST':
        stockname  = request.POST['stockname']
        query = request.POST['askquery']
        if len(query) < 5 :
            messages.error(request, "Please describe your query correctly.")
        else:
            queryform = Query(query=query, stockname=stockname)
            queryform.save()
            messages.success(request, "Your message has been successfully sent")

    return redirect('main-view')


# Authentication APIs
def handlesignup(request):
    if request.method == 'POST':
        # Get the Post parametres
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['pass2']


        # check for errorneous input
        if len(username) > 20:
            messages.error(request, "Username must be under 20 characters")
            return redirect('main-view')

        if " " in username:
            messages.error(request, "Username cannot contain spaces")
            return redirect('main-view')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('main-view')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Uername already exists. Choose unique username")
            return redirect('main-view')
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists. Please Log in")
            return redirect('main-view')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.save()
        messages.success(request, "Your account has been created successfully. You can login now.")
        return redirect('main-view')

    else:
        return HttpResponse("404 - Not Found")

def handlelogin(request):
    if request.method == 'POST':
        # Get the Post parametres
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('main-view')
        else:
            messages.error(request, "Invalid Credentials: Please try again")
            return redirect('main-view')
    return HttpResponse('404 not found')

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('main-view')
