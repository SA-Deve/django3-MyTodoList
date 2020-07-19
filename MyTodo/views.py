from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import TodoForm
from .models import TodoModel
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'GET':
        context = {'form': UserCreationForm()}
        return render(request, 'html/signup.html', context)
    else:
        if request.POST['password1']  == request.POST['password2']:
            try:
                user = User.objects.create_user(
                username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                context = {'form': UserCreationForm(),'error':'Please take another user'}
                return render(request, 'html/signup.html', context)
        else:
            context = {'form': UserCreationForm(), 'error': 'Password do not match'}
            return render(request, 'html/signup.html', context)


@login_required
def home(request):
    todos = TodoModel.objects.filter(user=request.user, dateCompleted__isnull=True)
    context = {'todos': todos}
    return render(request, 'html/home.html', context)


@login_required
def completedTodos(request):
    todos = TodoModel.objects.filter(user=request.user, dateCompleted__isnull=False)
    context = {'todos': todos}
    return render(request, 'html/completedTodos.html', context)

@login_required
def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signup')

def loginUser(request):
    if request.method == 'GET':
        context = {'form': AuthenticationForm()}
        return render(request, 'html/login.html', context)
    else:
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is None:
            context = {'form': AuthenticationForm(
            ), 'error': 'Username/Password do not match'}
            return render(request, 'html/login.html', context)
        else:
            login(request, user)
            return redirect('home')


@login_required
def createTodo(request):
    if request.method == 'GET':
        context = {'form': TodoForm()}
        return render(request, 'html/createTodo.html', context)
    else:
        try:
            form = TodoForm(request.POST)
            newTodo = form.save(commit=False)
            newTodo.user = request.user
            newTodo.save()
            return redirect('home')
        except ValueError:
            context = {'form': TodoForm(),'error':'Bad data. Try again.'}
            return render(request, 'html/createTodo.html', context)


@login_required
def viewTodo(request,todo_id):
    todos = TodoModel.objects.get(id=todo_id,user=request.user)
    if request.method == 'GET':
        todoForm = TodoForm(instance=todos)
        context = {'todos': todos, 'todoForm': todoForm}
        return render(request, 'html/viewTodo.html', context)
    else:
        try:
            form = TodoForm(request.POST,instance=todos)
            form.save()
            return redirect('home')
        except ValueError:
            context = {'todos': todos, 'todoForm': todoForm,'error':'Bad Info'}
            return render(request, 'html/viewTodo.html', context)


@login_required
def completeTodo(request,todo_id):
    todos = TodoModel.objects.get(id=todo_id, user=request.user)
    if request.method == 'POST':
        todos.dateCompleted = timezone.now()
        todos.save()
        return redirect('home')


@login_required
def deleteTodo(request, todo_id):
    todos = TodoModel.objects.get(id=todo_id, user=request.user)
    if request.method == 'POST':
        todos.delete()
        return redirect('home')
        

        
    
