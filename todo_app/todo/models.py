from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class TodoModel(models.Model):
    title = models.CharField(max_length=200)
    important = models.BooleanField(default=False)
    done = models.BooleanField(default=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo:view_certain_todo', args=[self.pk])


class CategoryModel(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo:view_by_category', args=[self.title])