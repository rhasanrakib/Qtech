from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . forms import SignUpForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from . models import UserSearchHistory
from django.contrib.auth.models import User
from django.db.models import Q

# @login_required(login_url='login')


@login_required
def homeView(request):
    context={}
    list_user = User.objects.all()
    context['users']=list_user
    user = User.objects.get(id=request.user.id)
    if 'search-box' in request.GET:
        #Get the search box value
        searchString = request.GET['search-box']
        
        #Split the string into words
        keyWords= searchString.lower().split()
        
        #Remove Duplicate Keywords
        for i in range(0,len(keyWords)-1):
            for j in range(i+1,len(keyWords)):
                if keyWords[i]==keyWords[j]:
                    keyWords.pop(j)

        #add string to the template search box and line
        context['searched_key']=searchString

        #add those words to the template
        #context['keyWords']=keyWords

        #Lower case the string so that we can search
        searchString = searchString.lower()
        
        #Filter matched data to show
        query = Q()
        wordCounts=Q()
        for words in keyWords:
            query = query | Q(searchKeyWords__contains=words)
        showData = UserSearchHistory.objects.filter(query).order_by('-createdTime')
        context['showData']=showData

        #Count the number of occurences of keywords in a dictionary
        keyWordsCount={}
        for i in keyWords:
            keyWordsCount[i]=UserSearchHistory.objects.filter(searchKeyWords__contains=i).count()
        context['keyWords']=keyWordsCount
        #Save string in database
        history = UserSearchHistory(searchKeyWords=searchString,owner=user)
        history.save()

    else:
        searchString=False

    return render(request, 'index.html',context)


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
