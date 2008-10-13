from django.db import models
from django import forms

# Create your models here.
class SearchForm(forms.Form):
   search_terms = forms.CharField(max_length=200)

