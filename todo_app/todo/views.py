from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import CategoryModel, TodoModel
from .forms import TodoForm, TodoUpdateForm
from django.contrib import messages
# Create your views here.


def home_page(request):
    return render(request, 'todo/home.html')



def signup_user(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'todo/signup_user.html', {'form':form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                messages.success(request, 'Your account was succesfully created')
                return redirect('todo:home_page')
            except IntegrityError:
                messages.error(request, 'Person with this nickname is already registered')
                return render(request, 'todo/signup_user.html', context={'form':UserCreationForm()})
        else:
            messages.error(request, 'You need to type in the exact same password twice')
            return render(request, 'todo/signup_user.html', context={'form':UserCreationForm()})


def login_user(request):
    form = AuthenticationForm()
    form.fields['username'].widget.attrs['class'] = "login__input"
    form.fields['password'].widget.attrs['class'] = "login__input"
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'No such user')
            return render(request, 'todo/login_user.html', context={'form': form})
        else:
            login(request, user)
            messages.success(request, 'Succesfully logged in')
            return redirect('todo:home_page')
    else:
        return render(request, 'todo/login_user.html', context={'form':form})


def logout_user(request):
    logout(request)
    messages.info(request, "You've been logged out. Please, log in if you want to proceed")
    return redirect('todo:login_user')

def view_my_todos(request):
    todos = TodoModel.objects.filter(user=request.user, done=False).order_by('-created_at')
    categorys = CategoryModel.objects.all()
    return render(request, 'todo/my_todos.html', context={'todos':todos, 'category':categorys})

def add_todo(request):
    if request.method == 'GET':
        form = TodoForm()
        return render(request, 'todo/add_todo.html', context={'form':form})
    else:
        form = TodoForm(request.POST)
        if form.is_valid():
            new_todo = TodoModel.objects.create(title=form.cleaned_data['title'], description=form.cleaned_data['description'], important=bool(request.POST.get('important', False)), category=form.cleaned_data['category'], user=request.user)
            new_todo.save()
            return redirect('todo:view_my_todos')
        else:
            return render(request, 'todo/add_todo.html', context={'form':form})

def update_todo(request, pk):
    todo = get_object_or_404(TodoModel, user=request.user, pk=pk)
    form = TodoUpdateForm(instance=todo)
    if request.method == 'GET':
        return render(request, 'todo/update_todo.html', context={'form':form, 'todo':todo})
    else:
        TodoModel.objects.filter(pk=pk, user=request.user).update(title=request.POST['title'], description=request.POST['description'], important=bool(request.POST.get('important', False)), done=bool(request.POST.get('done', False)), category=request.POST['category'])
        return redirect('todo:view_my_todos')

    # def update_todo(request, pk):
    # todo = get_object_or_404(TodoModel, user=request.user, pk=pk)
    # form = TodoForm(instance=todo)
    # if request.method == 'GET':
    #     return render(request, 'todo/update_todo.html', context={'form':form, 'todo':todo})
    # else:
    #     TodoModel.objects.filter(pk=pk, user=request.user).update(title=request.POST['title'], description=request.POST['description'], important=bool(request.POST.get('important', False)))
    #     return redirect('todo:view_my_todos')

def delete_todo(request, pk):
    de = get_object_or_404(TodoModel, user=request.user, pk=pk)
    messages.success(request, f'{de.title} succesfully deleted')
    de.delete()
    return redirect('todo:view_my_todos')

def view_certain_todo(request, pk):
    todo = get_object_or_404(TodoModel, pk=pk)
    return render(request, 'todo/view_certain_todo.html', context={'todo':todo})

def view_by_category(request, title):
    todos = TodoModel.objects.filter(category=CategoryModel.objects.get(title=title), user=request.user).select_related('category')
    return render(request, 'todo/todo_by_category.html', context={'todos':todos})

def completed(request):
    todos = TodoModel.objects.filter(user=request.user, done=True)
    return render(request, 'todo/completed.html', context={'todos':todos})


def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('todo:home_page')
    else:
        return redirect('todo:login_user')

