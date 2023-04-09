
from django import forms
from .models import TodoModel

class TodoForm(forms.ModelForm):
    # title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class":"w-25 form-control"}))
    # description = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={"class":"w-50 r-5 form-control"}))
    important = forms.BooleanField(required=False)
    class Meta():
        model = TodoModel
        fields = ["title", "description", 'important', 'category']
        widgets = {
                "title" : forms.TextInput(attrs={"class":"w-25 form-control"}),
                "description" : forms.Textarea(attrs={"class":"w-50 r-5 form-control"}),
                'category' : forms.Select(attrs={"class":"w-50 r-5 form-control"})
            }

class TodoUpdateForm(TodoForm):
    done = forms.BooleanField(required=False)
    fields = ["title", "description", 'important', 'category' 'done']