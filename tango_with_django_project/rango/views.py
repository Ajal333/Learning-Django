from django.http import HttpResponse
from django.shortcuts import render
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from rango.models import Category,Page
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def index(request) :
    cat_list =  Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':cat_list,'pages':page_list}
    return render(request, 'rango/index.html', context = context_dict)

def about(request) :
    context_dict = {'name' : "Ajal"}
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request,category_name_slug) :

    context_dict = {}

    try :
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist :
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html',context_dict)

@login_required
def add_category(request) :
    form = CategoryForm()

    if request.method == 'POST' :
        form = CategoryForm(request.POST)

        if form.is_Valid() :
            form.save(commit = True)

            return index(request)
        
        else :
            print(form.errors)
        
    return render(request, 'rango/add_category.html',{'form':form})

@login_required
def add_page(request,category_name_slug) :
    try : 
        category = Category.objects.get(slug = category_name_slug)
            
    except Category.DoesNotExist :
        category = None

    form = PageForm()

    if request.method == 'POST' :
        form = PageForm(request.POST)

        if form.is_Valid() :
            if category :
                page = form.save(commit = True)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request,category_name_slug)
            else :
                print(form.errors)
        
       
    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html',context_dict)

def register(request) :
    registered = False

    if request.method == 'POST' : 
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)
        
        if user_form.is_valid() and profile_form.is_valid() :
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            if 'picture' in request.FILES :
                profile.picture = request.FILES['picture']
                profile.save()

                registered = True
        
        else :
            print(user_form.errors,profile_form.errors)

    else :
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form' : user_form, 'profile_form':profile_form, 'registered':registered}
    return render(request,'rango/register.html',context_dict)

def user_login(request) :
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user :
            if user.is_active :
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else :
                return HttpResponse('Your account is Disabled')
        else :
            print('Invalid login details: {0} , {1}'.format(username,password))
            return HttpResponse('Invalid Login Details')
    else :
        return render(request,'rango/login.html',{})

@login_required
def restricted(request) :
    return HttpResponse('You can see this message if you are logged in!')

@login_required
def user_logout(request) :
    logout(request)
    retrun HttpResponseRedirect(reverse('index'))

