"""
URL configuration for the marketplace app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.HomeView.as_view(), name="home_redirect"),
    
    # Freelancer browsing
    path("freelancers/", views.FreelancerListView.as_view(), name="freelancer_list"),
    path("freelancers/search/", views.FreelancerSearchHTMXView.as_view(), name="freelancer_search"),
    
    # Portfolio management
    path("portfolio/add/", views.PortfolioCreateView.as_view(), name="portfolio_add"),
    path("portfolio/<int:pk>/edit/", views.PortfolioUpdateView.as_view(), name="portfolio_edit"),
    path("portfolio/<int:pk>/delete/", views.PortfolioDeleteView.as_view(), name="portfolio_delete"),
    path("portfolio/manage/", views.manage_portfolio, name="manage_portfolio"),
]
