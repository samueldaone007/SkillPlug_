"""
Forms for the marketplace app.
"""

from django import forms
from .models import PortfolioItem


class PortfolioItemForm(forms.ModelForm):
    """Form for adding/editing portfolio items."""
    
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "Project title",
        }),
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all resize-none",
            "placeholder": "Describe the project, your role, and technologies used...",
            "rows": 4,
        }),
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "accept": "image/*",
        }),
    )
    project_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all",
            "placeholder": "https://...",
        }),
    )
    
    class Meta:
        model = PortfolioItem
        fields = ["title", "description", "image", "project_url"]
