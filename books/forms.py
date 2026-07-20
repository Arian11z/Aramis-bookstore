from django import forms
from .models import Review, Rating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'نظر خود را درباره این کتاب بنویسید...',
                'rows': 5
            })
        }
        labels = {
            'comment': 'نظر شما'
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.RadioSelect(choices=[(i, f'{i} ستاره') for i in range(1, 6)])
        }
        labels = {
            'score': 'امتیاز شما'
        }