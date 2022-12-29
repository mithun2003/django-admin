from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache,cache_control
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.contrib import messages



@never_cache
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(
                    request, 'Profile created successfully' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'signup.html', context)


@never_cache
def loginPage(request):
    if 'username' in request.session:
        return redirect('home')
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['username'] = username

                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@never_cache
def index(request):
    if 'username' in request.session:
        dict_docs = {
            'posts': Post.objects.all()
        }
        return render(request, 'home.html', dict_docs)
    return redirect('login')


@login_required(login_url='login')
@never_cache
def about(request):
    return render(request, 'about.html')


@login_required(login_url='login')
@never_cache
def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='login')
@never_cache
def post(request):
    return render(request, 'post.html')



@never_cache
def admin_login(request):
    if 'username' in request.session:
        return redirect('showuser')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            return render(request, 'admin/admin-login.html')
        user_obj = authenticate(username=username, password=password)

        if user_obj and user_obj.is_superuser:
            request.session["username"] = username
            return redirect('showuser')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return render(request, 'admin/admin-login.html')

    else:
        return render(request, 'admin/admin-login.html')
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
#@never_cache
def logoutad(request):
    if 'username' in request.session:
        #print(request.session['username'])
        #del request.session['username']
        request.session.flush()
    logout(request)
    return redirect('admin1')

#@login_required(login_url='admin1')
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def show_users(request):
    # show all users in a table
    if 'username' in request.session:
        users = User.objects.all()            
        return render(request, 'admin/admin.html', {'dets': users})
    return redirect('admin1')


@never_cache
def edit_user(request,id):
    # edit user in database
    if 'username' in request.session:
        user = User.objects.get(id=id)
        if request.method == "POST":
            user_data = User.objects.filter(id=id).all()
            user_name = request.POST['username']
            email = request.POST['email']
            # password1=request.POST['password']
            # eny_password=pbkdf2_sha256.encrypt(password1,rounds=12000,salt_size=32)
            if User.objects.filter(username=user).exists():
                return redirect('showuser')
            if User.objects.filter(username=user_name).exists():
                messages.success(
                    request, 'Usename already exists')
                return render(request, 'admin/edit_user_form.html',{'user': user})
           
            for user in user_data:
                user.email = email
                user.username = user_name
                # if len(password1)<12:
                #     user.password = eny_password
                user.save()
            return redirect('showuser')
        else:
            return render(request, 'admin/edit_user_form.html', {'user': user})
    else:
        return redirect('admin1')


@never_cache
def delete_user(request,id):
    # delete user in database
    if 'username' in request.session:
        the_user = User.objects.filter(id=id).all()
        the_user.delete()
        return redirect('showuser')
    else:
        return redirect('admin1')


def searched_user(request):
    # for searching user in database
    if request.method == 'POST':
        data = request.POST['search']
        user_data = User.objects.filter(username__contains=data).all()
        if user_data:
            return render(request, 'admin/admin.html', {'dets': user_data, 'data1': data})
        else:
            msg = "No data found"
            return render(request, 'admin/admin.html', {'m': msg})
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
#@login_required
@never_cache
def make(request):
    return render(request, 'admin/create.html')
#@login_required(login_url='admin1')
@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@never_cache
def create(request): 
    if request.user.is_authenticated:
            return redirect('showuser')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(
                    request, 'Profile created successfully' + user)
                return redirect('showuser')

        context = {'form': form}
        return render(request, 'admin/create.html', context)
