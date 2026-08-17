"""
URL configuration for the reviews app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path(
        "freelancer/<str:username>/review/",
        views.create_review,
        name="create_review",
    ),
]
