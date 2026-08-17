"""
Models for the marketplace app.
Portfolio items and related functionality.
"""

from django.db import models
from django.urls import reverse
from django.conf import settings


class PortfolioItem(models.Model):
    """
    Represents a portfolio item showcasing a student's work.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio_items",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(
        blank=True,
        help_text="Describe the project, your role, and the outcome",
    )
    image = models.ImageField(
        upload_to="portfolio/",
        help_text="Upload a screenshot or image of your work",
    )
    project_url = models.URLField(
        blank=True,
        help_text="Link to live project or repository",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("portfolio_detail", kwargs={"pk": self.pk})
