from django import forms
from .models import MoviePetition

class MoviePetitionForm(forms.ModelForm):
    class Meta:
        model = MoviePetition
        fields = ['title', 'description']