from django import forms 
from .models import Post , Comment 
class CommentForm(forms.ModelForm):
    class Meta :
        model = Comment 
        fields = ['title','email','body']
        
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=120,widget=forms.widgets.EmailInput)
    to = forms.EmailField(max_length=120)
    comments = forms.CharField(required=False,max_length=200,widget=forms.widgets.Textarea)
class SearchForm(forms.Form):
    query = forms.CharField()