from django import forms
from .models import ReviewRating


class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
    
    # def __init__(self, *args, **kwargs):
    #     super(ReviewRatingForm, self).__init__(*args, **kwargs)
    #     self.fields['subject'].widget.attrs['placeholder'] = "Enter Subject"
    #     self.fields['review'].widget.attrs['placeholder'] = "Write your review"
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = "form-control"
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': 'Enter Subject',
                'class': 'form-control'
            }),
            'review': forms.Textarea(attrs={
                'placeholder': 'Enter Review',
                "rows": 3,
                'class': 'form-control'
            })
        }
