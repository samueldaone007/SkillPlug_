"""
Views for the jobs app.
Handles job posting, browsing, and applications.
"""
 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
 
from apps.accounts.models import User, Skill
from .models import Job, Application
from .forms import JobPostForm, JobApplicationForm, JobStatusForm
 
 
class JobListView(ListView):
    """Browse all active job postings."""
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Job.objects.filter(
            is_active=True,
            status__in=["open", "in_progress"],
        ).select_related("posted_by").prefetch_related("required_skills").annotate(
            applications_total=Count("applications"),
        )
        
        # Search
        search = self.request.GET.get("search", "")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(required_skills__name__icontains=search)
            ).distinct()
        
        # Filter by budget type
        budget_type = self.request.GET.get("budget_type", "")
        if budget_type:
            queryset = queryset.filter(budget_type=budget_type)
        
        # Filter by skill
        skill = self.request.GET.get("skill", "")
        if skill:
            queryset = queryset.filter(required_skills__name=skill)
        
        return queryset.order_by("-created_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Job Board"
        context["skills"] = Skill.objects.filter(is_active=True)
        context["budget_types"] = Job.BUDGET_TYPE_CHOICES
        context["search_query"] = self.request.GET.get("search", "")
        return context
 
 
class JobDetailView(DetailView):
    """View job details and apply."""
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.object
        user = self.request.user
        
        # Application form for authenticated students
        if user.is_authenticated and user.is_student:
            has_applied = Application.objects.filter(
                student=user,
                job=job,
            ).exists()
            context["has_applied"] = has_applied
            if not has_applied and job.status == "open":
                context["form"] = JobApplicationForm(user=user, job=job)
        else:
            context["has_applied"] = False
        
        # Applications (visible to job poster)
        if user.is_authenticated and job.posted_by == user:
            context["applications"] = job.applications.select_related("student").all()
        
        # Status form for job poster
        if user.is_authenticated and job.posted_by == user:
            context["status_form"] = JobStatusForm(instance=job)
        
        context["title"] = f"{job.title} - SkillPlug Jobs"
        return context
 
 
class JobCreateView(CreateView):
    """Post a new job."""
    model = Job
    form_class = JobPostForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job_list")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to post a job.")
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, "Job posted successfully!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Post a Job"
        context["action"] = "Post"
        return context
 
 
class JobUpdateView(UpdateView):
    """Edit an existing job."""
    model = Job
    form_class = JobPostForm
    template_name = "jobs/job_form.html"
    success_url = reverse_lazy("job_list")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        job = self.get_object()
        if job.posted_by != request.user and not request.user.is_staff:
            messages.error(request, "You can only edit your own job posts.")
            return redirect("job_detail", pk=job.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "Job updated successfully!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Job"
        context["action"] = "Update"
        return context
 
 
class JobDeleteView(DeleteView):
    """Delete a job posting."""
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    success_url = reverse_lazy("job_list")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        job = self.get_object()
        if job.posted_by != request.user and not request.user.is_staff:
            messages.error(request, "You can only delete your own job posts.")
            return redirect("job_detail", pk=job.pk)
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Job deleted successfully!")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Job"
        return context
 
 
@login_required
def apply_job(request, pk):
    """Handle job application submission."""
    job = get_object_or_404(Job, pk=pk, status="open", is_active=True)
    
    if not request.user.is_student:
        messages.error(request, "Only students can apply for jobs.")
        return redirect("job_detail", pk=pk)
    
    if job.posted_by == request.user:
        messages.error(request, "You cannot apply to your own job.")
        return redirect("job_detail", pk=pk)
    
    # Check if already applied
    if Application.objects.filter(student=request.user, job=job).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect("job_detail", pk=pk)
    
    if request.method == "POST":
        form = JobApplicationForm(
            request.POST,
            user=request.user,
            job=job,
        )
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.job = job
            application.save()
            messages.success(request, "Application submitted successfully!")
            
            if request.headers.get("HX-Request"):
                return render(request, "partials/application_success.html", {
                    "job": job,
                })
            return redirect("job_detail", pk=pk)
    else:
        form = JobApplicationForm(user=request.user, job=job)
    
    return render(request, "jobs/job_application_form.html", {
        "form": form,
        "job": job,
        "title": f"Apply - {job.title}",
    })
 
 
@login_required
def update_application_status(request, pk, status):
    """Update application status (accept/reject)."""
    application = get_object_or_404(Application, pk=pk)
    job = application.job
    
    # Only job poster can update status
    if job.posted_by != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to update this application.")
        return redirect("job_detail", pk=job.pk)
    
    if status in ["accepted", "rejected", "pending"]:
        application.status = status
        application.save()
        messages.success(request, f"Application {status}.")
    
    return redirect("job_detail", pk=job.pk)
 
 
@login_required
def my_jobs(request):
    """View jobs posted by the current user."""
    jobs = Job.objects.filter(
        posted_by=request.user,
    ).annotate(
        applications_total=Count("applications"),
    ).order_by("-created_at")
    
    context = {
        "jobs": jobs,
        "title": "My Job Posts",
    }
    return render(request, "jobs/my_jobs.html", context)
 
 
@login_required
def my_applications(request):
    """View applications submitted by the current user."""
    applications = Application.objects.filter(
        student=request.user,
    ).select_related("job").order_by("-created_at")
    
    context = {
        "applications": applications,
        "title": "My Applications",
    }
    return render(request, "jobs/my_applications.html", context)
 
 
@login_required
def update_job_status(request, pk):
    """Update job status via form submission."""
    job = get_object_or_404(Job, pk=pk)
    
    if job.posted_by != request.user and not request.user.is_staff:
        messages.error(request, "You can only update your own jobs.")
        return redirect("job_detail", pk=pk)
    
    if request.method == "POST":
        form = JobStatusForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job status updated!")
    
    return redirect("job_detail", pk=pk)