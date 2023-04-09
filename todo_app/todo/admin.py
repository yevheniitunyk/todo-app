from django.contrib import admin
from .models import TodoModel, CategoryModel
# Register your models here.


admin.site.register(TodoModel)
admin.site.register(CategoryModel)