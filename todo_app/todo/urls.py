from django.urls import include, path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('', login_redirect, name='start'),
    path('home/', home_page, name='home_page'),
    path('signup/', signup_user, name='signup_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('todo/<int:pk>', view_certain_todo, name='view_certain_todo'),
    path('update/<int:pk>', update_todo, name='update_todo'),
    path('delete/<int:pk>', delete_todo, name='delete_todo'),
    path('my_todos', view_my_todos, name='view_my_todos'),
    path('my_todos/add/', add_todo, name='add_todo'),
    path('my_todos/completed_todos', completed, name='completed'),
    path('my_todos/category/<str:title>', view_by_category, name='view_by_category')
]