from django.urls import path
from . import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutUser, name='logout'),
    path('login/', views.loginUser, name='login'),
    path('create/', views.createTodo, name='createTodo'),
    path('viewTodo/<int:todo_id>/', views.viewTodo, name='viewTodo'),
    path('completedTodos/', views.completedTodos, name='completedTodos'),
    path('completeTodo/<int:todo_id>/', views.completeTodo, name='completeTodo'),
    path('deleteTodo/<int:todo_id>/',views.deleteTodo, name='deleteTodo')
]
