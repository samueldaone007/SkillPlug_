"""
URL configuration for the jobs app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Job browsing
    path("", views.JobListView.as_view(), name="job_list"),
    path("<int:pk>/", views.JobDetailView.as_view(), name="job_detail"),
    
    # Job management
    path("post/", views.JobCreateView.as_view(), name="job_post"),
    path("<int:pk>/edit/", views.JobUpdateView.as_view(), name="job_edit"),
    path("<int:pk>/delete/", views.JobDeleteView.as_view(), name="job_delete"),
    path("<int:pk>/status/", views.update_job_status, name="job_status_update"),
    
    # Applications
    path("<int:pk>/apply/", views.apply_job, name="job_apply"),
    path(
        "application/<int:pk>/status/<str:status>/",
        views.update_application_status,
        name="application_status",
    ),
    
    # User-specific views
    path("my-jobs/", views.my_jobs, name="my_jobs"),
    path("my-applications/", views.my_applications, name="my_applications"),
]
