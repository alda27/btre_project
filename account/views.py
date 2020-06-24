from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from contacts.models import Contact


# Create your views here.


def register(request):
    if request.user.is_authenticated:
        messages.error(request, 'you cant do this')
        return redirect('index')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']

            # validations
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username is taken')
                    return redirect('register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Email is taken')
                        return redirect('register')
                    else:
                        user = User.objects.create_user(username=username, password=password, email=email,
                                                        first_name=first_name, last_name=last_name)
                        user.save()
                        messages.success(request, 'Now you are registered')
                        return redirect('login')
            else:
                messages.error(request, 'Passwords not match')
                return redirect('register')
        else:
            return render(request, 'accounts/register.html')


def login(request):
    if request.user.is_authenticated:
        messages.error(request, 'you are logged in')
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Username or Password incorrect')
        return render(request, 'accounts/login.html')


@login_required()
def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    # user_contacts_count = Contact.objects.all().filter(user_id=request.user.id).count()
    context = {'contacts': user_contacts}
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')
