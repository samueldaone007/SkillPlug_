"""
Forms for the reviews app.
"""

from django import forms
from .models import Review


RATING_CHOICES = [
    (5, "5 - Excellent"),
    (4, "4 - Very Good"),
    (3, "3 - Good"),
    (2, "2 - Fair"),
    (1, "1 - Poor"),
]


class ReviewForm(forms.ModelForm):
    """Form for creating a review."""
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        initial=5,
        widget=forms.RadioSelect(attrs={
            "class": "sr-only peer",
        }),
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all resize-none",
            "placeholder": "Share your experience working with this freelancer...",
            "rows": 4,
        }),
    )
    
    class Meta:
        model = Review
        fields = ["rating", "comment"]
    
    def __init__(self, *args, reviewer=None, freelancer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reviewer = reviewer
        self.freelancer = freelancer
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if user already reviewed this freelancer
        if self.reviewer and self.freelancer:
            if Review.objects.filter(
                reviewer=self.reviewer,
                freelancer=self.freelancer,
            ).exists():
                raise forms.ValidationError("You have already reviewed this freelancer.")
            
            if self.reviewer == self.freelancer:
                raise forms.ValidationError("You cannot review yourself.")
        
        return cleaned_data
    
    def save(self, commit=True):
        review = super().save(commit=False)
        review.reviewer = self.reviewer
        review.freelancer = self.freelancer
        if commit:
            review.save()
        return review
