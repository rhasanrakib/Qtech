from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from . forms import SignUpForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from . models import UserSearchHistory
from django.contrib.auth.models import User
from django.db.models import Q
import json
from django.http import JsonResponse
from django.core import serializers
from django.utils import timezone
from datetime import date, timedelta


@login_required
@csrf_exempt
def homeView(request):
    context = {}
    user = User.objects.get(id=request.user.id)
    calenderMax = date.today().strftime("%Y-%m-%d")
    context['calenderMax'] = calenderMax
    list_user = User.objects.all()
    context['users'] = list_user
    if 'search-box' in request.GET:

        # Get the search box value
        searchString = request.GET['search-box']

        if searchString is not "":
            # Save string in database
            history = UserSearchHistory.objects.create(
                searchKeyWords=searchString, owner=user)

        # Split the string into words
        keyWords = searchString.lower().split()

        # Remove Duplicate Keywords
        for i in range(0, len(keyWords)-1):
            for j in range(i+1, len(keyWords)):
                if keyWords[i] == keyWords[j]:
                    keyWords.pop(j)

        # add string to the template search box and line
        context['searched_key'] = searchString

        # Lower case the string so that we can search
        searchString = searchString.lower()

        # Filter matched data to show
        query = Q()
        for words in keyWords:
            query = query | Q(searchKeyWords__contains=words)
        showData = UserSearchHistory.objects.filter(
            query).order_by('-createdTime')
        context['showData'] = showData

        # Count the number of occurences of keywords in a dictionary
        keyWordsCount = {}
        for i in keyWords:
            keyWordsCount[i] = UserSearchHistory.objects.filter(
                searchKeyWords__contains=i).count()
        # add those words to the template
        context['keyWords'] = keyWordsCount

    else:
        searchString = False

    # Ajax Request
    if request.is_ajax and request.method == "POST":
        context = {}
        # Receive the Ajax from getSelectedData dict key
        getSelectedData = request.POST.getlist(
            'getSelectedData', request.POST.getlist('getSelectedData[]'))

        # loads the Json
        for i in getSelectedData:
            data = json.loads(i)

        # Get The Value of these Items
        getKeywords = data['keywords']
        getUsers = data['users']
        getTime = data['time']
        getDate = data['date']

        # If date is empty then select all the data

        if getDate[0] is "":
            getDate[0] = "2020-03-01"
        if getDate[1] is "":
            getDate[1] = calenderMax
        getDate[1]+=" 23:59:59"
        # Keywords Query
        queryWords = Q()
        for words in getKeywords:
            queryWords = queryWords | Q(searchKeyWords__contains=words)

        # Users Query
        queryUser = Q()

        for user in getUsers:
            queryUser = queryUser | Q(owner=User.objects.get(username=user))
            #query = query | Q(owner=user)
        # Time Query
        queryTime = Q()
        today = date.today()

        for time in getTime:
            if time is 'yesterday':
                yesterday = today - timedelta(days=1)
                queryTime = queryTime | Q(createdTime__date=yesterday)
            elif time is 'last_week':
                lastweek = today - timedelta(weeks=1)
                queryTime = queryTime | Q(createdTime__week=lastweek)
            elif time is 'last_month':
                lastmonth = today - timedelta(days=30)
                queryTime = queryTime | Q(createdTime__month=lastmonth)

        # Date Query mixed with Time
        queryTime = queryTime | Q(createdTime__range=[getDate[0], getDate[1]])

        # Filter from all these queries
        filterData = UserSearchHistory.objects.filter(
            queryUser & queryWords & queryTime).order_by('-createdTime')

        # Serialize data cause this is query not Dictionary
        data = serializers.serialize('json', filterData)
        lst_user=serializers.serialize('json', list_user)
        # Return the Response to the templates
        return JsonResponse({'instance': data,'user':lst_user}, status=200, safe=False)

    return render(request, 'index.html', context)


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
            # mail = authenticate(request, email=email, password=password)

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
