from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . forms import SignUpForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# @login_required(login_url='login')


@login_required
def homeView(request):
    return render(request, 'index.html')


def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Failed Submission')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
def loginView(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            #mail = authenticate(request, email=email, password=password)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                isValidUser = True
                login(request, user)
                return redirect("home")

        context = {}
        return render(request, 'login.html', context)


def log_out(request):
    logout(request)
    # return redirect("posts:post_home")
    return redirect("/")
