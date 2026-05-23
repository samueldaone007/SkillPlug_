"""
Views for the marketplace app.
Handles freelancer browsing, search, portfolio management, and the home page.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy

from apps.accounts.models import User, Skill
from .models import PortfolioItem
from .forms import PortfolioItemForm


class HomeView(TemplateView):
    """Home page with featured freelancers and stats."""
    template_name = "marketplace/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Featured freelancers (verified and available)
        context["featured"] = User.objects.filter(
            verified=True,
            availability_status="available",
            profile_complete=True,
        ).select_related().prefetch_related("skills")[:6]
        
        # Top-rated freelancers
        top_rated = User.objects.filter(
            profile_complete=True,
            reviews_received__isnull=False,
        ).annotate(
            avg_rating=Avg("reviews_received__rating"),
            review_count=Count("reviews_received"),
        ).order_by("-avg_rating")[:4]
        context["top_rated"] = top_rated
        
        # Recently joined
        context["recent"] = User.objects.filter(
            profile_complete=True,
        ).select_related().prefetch_related("skills")[:4]
        
        # Stats
        context["total_freelancers"] = User.objects.filter(
            profile_complete=True
        ).count()
        context["verified_freelancers"] = User.objects.filter(
            profile_complete=True,
            verified=True,
        ).count()
        context["total_skills"] = Skill.objects.filter(is_active=True).count()
        
        # Available skills for search
        context["skills"] = Skill.objects.filter(is_active=True)[:12]
        
        # Nigerian universities for filter
        context["universities"] = User.NIGERIAN_UNIVERSITIES[:8]
        
        context["title"] = "SkillPlug - Connect with Student Talent"
        return context


class FreelancerListView(ListView):
    """Browse and search student freelancers."""
    model = User
    template_name = "marketplace/freelancer_list.html"
    context_object_name = "freelancers"
    paginate_by = 12
    
    def get_queryset(self):
        queryset = User.objects.filter(
            profile_complete=True,
        ).prefetch_related("skills").annotate(
            avg_rating=Avg("reviews_received__rating"),
            review_count=Count("reviews_received"),
        )
        
        # Search
        search = self.request.GET.get("search", "")
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(bio__icontains=search) |
                Q(department__icontains=search) |
                Q(skills__name__icontains=search)
            ).distinct()
        
        # Filter by school
        school = self.request.GET.get("school", "")
        if school:
            queryset = queryset.filter(school=school)
        
        # Filter by skill
        skill = self.request.GET.get("skill", "")
        if skill:
            queryset = queryset.filter(skills__name=skill)
        
        # Filter by availability
        availability = self.request.GET.get("availability", "")
        if availability:
            queryset = queryset.filter(availability_status=availability)
        
        # Filter by verified only
        if self.request.GET.get("verified") == "true":
            queryset = queryset.filter(verified=True)
        
        # Sorting
        sort = self.request.GET.get("sort", "recent")
        if sort == "rating":
            queryset = queryset.order_by("-avg_rating")
        elif sort == "name":
            queryset = queryset.order_by("full_name")
        else:
            queryset = queryset.order_by("-date_joined")
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Browse Freelancers"
        context["skills"] = Skill.objects.filter(is_active=True)
        context["universities"] = User.NIGERIAN_UNIVERSITIES
        context["availability_choices"] = User.AVAILABILITY_CHOICES
        
        # Preserve filter parameters for pagination
        query_params = self.request.GET.copy()
        if "page" in query_params:
            query_params.pop("page")
        context["query_params"] = query_params.urlencode()
        context["search_query"] = self.request.GET.get("search", "")
        
        return context


class FreelancerSearchHTMXView(ListView):
    """HTMX-powered live search for freelancers."""
    model = User
    template_name = "partials/freelancer_search_results.html"
    context_object_name = "freelancers"
    paginate_by = 8
    
    def get_queryset(self):
        queryset = User.objects.filter(
            profile_complete=True,
        ).prefetch_related("skills").annotate(
            avg_rating=Avg("reviews_received__rating"),
        )
        
        search = self.request.GET.get("search", "")
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(bio__icontains=search) |
                Q(skills__name__icontains=search)
            ).distinct()
        
        # Filter by skill (for HTMX requests)
        skill = self.request.GET.get("skill", "")
        if skill:
            queryset = queryset.filter(skills__name=skill)
        
        school = self.request.GET.get("school", "")
        if school:
            queryset = queryset.filter(school=school)
        
        return queryset.order_by("-date_joined")[:12]


class PortfolioCreateView(CreateView):
    """Add a new portfolio item."""
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = "marketplace/portfolio_form.html"
    success_url = reverse_lazy("dashboard")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Portfolio item added successfully!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add Portfolio Item"
        context["action"] = "Create"
        return context


class PortfolioUpdateView(UpdateView):
    """Edit an existing portfolio item."""
    model = PortfolioItem
    form_class = PortfolioItemForm
    template_name = "marketplace/portfolio_form.html"
    success_url = reverse_lazy("dashboard")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        portfolio = self.get_object()
        if portfolio.user != request.user:
            messages.error(request, "You can only edit your own portfolio items.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "Portfolio item updated successfully!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Portfolio Item"
        context["action"] = "Update"
        return context


class PortfolioDeleteView(DeleteView):
    """Delete a portfolio item."""
    model = PortfolioItem
    template_name = "marketplace/portfolio_confirm_delete.html"
    success_url = reverse_lazy("dashboard")
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account_login")
        portfolio = self.get_object()
        if portfolio.user != request.user:
            messages.error(request, "You can only delete your own portfolio items.")
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Portfolio item deleted successfully!")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Portfolio Item"
        return context


@login_required
def manage_portfolio(request):
    """View to manage all portfolio items."""
    portfolio_items = request.user.portfolio_items.all()
    context = {
        "portfolio_items": portfolio_items,
        "title": "Manage Portfolio",
    }
    return render(request, "marketplace/manage_portfolio.html", context)
