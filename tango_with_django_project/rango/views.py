from django.http import HttpResponse
from django.shortcuts import render,redirect
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from rango.models import Category,Page,User,UserProfile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

def index(request) :
    request.session.set_test_cookie()
    cat_list =  Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories':cat_list,'pages':page_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    response = render(request, 'rango/index.html', context = context_dict)
    return response

def about(request) :
    context_dict = {'name' : "Ajal"}
    if request.session.test_cookie_worked() :
        print('Test Cookie Worked')
        request.session.delete_test_cookie()

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request,category_name_slug) :

    context_dict = {}

    try :
        category = Category.objects.get(slug=category_name_slug)

        pages = Page.objects.filter(category=category).order_by('-views')

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

        if form.is_valid() :
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
    return HttpResponseRedirect(reverse('index'))

def get_server_side_cookie(request,cookie,default_val=None) :
    val = request.session.get(cookie)
    if not val :
        val = default_val
    return val

def visitor_cookie_handler(request) :
    visits = int(get_server_side_cookie(request,'visists','1'))

    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time =   datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 1 :
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else :
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def track_url(request) :
    page_id = None
    url = '/rango/'
    if request.method == 'GET' :
        if page_id in request.GET :
            page_id = request.GET['page_id']

            try :
                page = Page.objects.get(id= page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except :
                pass
    return redirect(url)

@login_required
def profile(request, username) :
    try :
        user = User.objects.get(username = username)
    except User.DoesNotExist :
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm(
        {'website': userprofile.website, 'picture': userprofile.picture})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    return render(request, 'rango/new_profile.html',{'userprofile': userprofile, 'selecteduser': user, 'form': form})

@login_required
def likes(request):
    cat_id = None
    if request.method == 'GET' :
        cat_id = request.GET['category_id']
        likes = 0
    if cat_id :
        category = Category.objects.get(id = int(cat_id))
        if category :
            likes = category.likes + 1
            category.likes = likes
            category.save()
    return HttpResponse(likes)
