"""
Context processors for the marketplace app.
Provides global template variables.
"""

from apps.accounts.models import User, Skill


def marketplace_stats(request):
    """Add marketplace statistics to all templates."""
    return {
        "total_freelancers": User.objects.filter(profile_complete=True).count(),
        "total_verified": User.objects.filter(profile_complete=True, verified=True).count(),
        "popular_skills": Skill.objects.filter(is_active=True)[:8],
    }
