"""
Views for the reviews app.
Handles creating and displaying reviews.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse

from apps.accounts.models import User
from .models import Review
from .forms import ReviewForm


class ReviewCreateView(CreateView):
    """Create a review for a freelancer."""
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to leave a review.")
            return redirect("account_login")
        
        self.freelancer = get_object_or_404(
            User,
            username=self.kwargs["username"],
            profile_complete=True,
        )
        
        # Cannot review yourself
        if self.freelancer == request.user:
            messages.error(request, "You cannot review yourself.")
            return redirect("freelancer_detail", username=self.freelancer.username)
        
        # Check if already reviewed
        if Review.objects.filter(
            reviewer=request.user,
            freelancer=self.freelancer,
        ).exists():
            messages.info(request, "You have already reviewed this freelancer.")
            return redirect("freelancer_detail", username=self.freelancer.username)
        
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["reviewer"] = self.request.user
        kwargs["freelancer"] = self.freelancer
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, "Review submitted successfully!")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("freelancer_detail", kwargs={"username": self.freelancer.username})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["freelancer"] = self.freelancer
        context["title"] = f"Review {self.freelancer.display_name}"
        return context


@login_required
def create_review(request, username):
    """Alternative function-based view for creating reviews."""
    freelancer = get_object_or_404(
        User,
        username=username,
        profile_complete=True,
    )
    
    if freelancer == request.user:
        messages.error(request, "You cannot review yourself.")
        return redirect("freelancer_detail", username=username)
    
    if Review.objects.filter(reviewer=request.user, freelancer=freelancer).exists():
        messages.info(request, "You have already reviewed this freelancer.")
        return redirect("freelancer_detail", username=username)
    
    if request.method == "POST":
        form = ReviewForm(
            request.POST,
            reviewer=request.user,
            freelancer=freelancer,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Review submitted successfully!")
            return redirect("freelancer_detail", username=username)
    else:
        form = ReviewForm(reviewer=request.user, freelancer=freelancer)
    
    return render(request, "reviews/review_form.html", {
        "form": form,
        "freelancer": freelancer,
        "title": f"Review {freelancer.display_name}",
    })
