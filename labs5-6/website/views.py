import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, SearchForm, KeywordForm
from .models import Record, Keyword
from nltk.tokenize import word_tokenize
from .utils import clean_text, add_record_to_corpus
from .forms import KeywordForm

def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('login')
    return render(request, 'home.html', {'records': records})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')

def add_record(request):
    if request.method == "POST":
        form = AddRecordForm(request.POST)
        if form.is_valid():
            new_record = form.save(commit=False)
            new_record.save()
            add_record_to_corpus(new_record)
            messages.success(request, "Record Added...")
            return redirect('home')
    else:
        form = AddRecordForm()
    return render(request, 'add_record.html', {'form': form})

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')

def search_records(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                query = form.cleaned_data['query']
                records = Record.objects.filter(content__icontains=query)
                return render(request, 'search_results.html', {'records': records})
            else:
                messages.error(request, "You must be logged in to search records.")
                return redirect('home')
    else:
        form = SearchForm()
    return render(request, 'search.html', {'form': form})



def save_keywords_to_json(request):
    file_path = 'keywords.json'
    keywords = read_json_file(file_path)
    keywords_list = list(keywords)
    with open(file_path, 'w') as f:
        json.dump(keywords_list, f, indent=4)
    return JsonResponse({'status': 'success'})

def add_keyword(request):
    if request.method == "POST":
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            add_keyword_to_json('keywords.json', [keyword])
            messages.success(request, "Keyword Added...")
            return redirect('home')
    else:
        form = KeywordForm()
    return render(request, 'add_keyword.html', {'form': form})

def update_keyword(request, index):
    file_path = 'keywords.json'
    if request.method == "POST":
        form = KeywordForm(request.POST)
        if form.is_valid():
            new_keyword = form.cleaned_data['keyword']
            update_keyword_in_json(file_path, index, [new_keyword])
            messages.success(request, "Keyword Updated...")
            return redirect('home')
    else:
        keywords = read_json_file(file_path)
        if 0 <= index < len(keywords):
            initial_data = {'keyword': keywords[index][0]}
            form = KeywordForm(initial=initial_data)
        else:
            form = KeywordForm()
            messages.error(request, "Invalid keyword index.")
    return render(request, 'update_keyword.html', {'form': form})

def delete_keyword(request, index):
    file_path = 'keywords.json'
    delete_keyword_from_json(file_path, index)
    messages.success(request, "Keyword Deleted...")
    return redirect('home')

