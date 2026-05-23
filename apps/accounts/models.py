"""
Custom User Model for SkillPlug
Extends AbstractUser with student-specific fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Skill(models.Model):
    """Represents a skill that students can offer."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon class")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
    
    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Custom User model for SkillPlug.
    Students and clients use the same model with different fields.
    """
    
    # Account types
    ACCOUNT_TYPE_CHOICES = [
        ("student", "Student Freelancer"),
        ("client", "Client"),
        ("both", "Both"),
    ]
    
    # Availability choices
    AVAILABILITY_CHOICES = [
        ("available", "Available for Work"),
        ("busy", "Currently Busy"),
        ("not_available", "Not Available"),
    ]
    
    # Nigerian universities (common ones)
    NIGERIAN_UNIVERSITIES = [
        ("unilag", "University of Lagos (UNILAG)"),
        ("ui", "University of Ibadan (UI)"),
        ("oau", "Obafemi Awolowo University (OAU)"),
        ("uniben", "University of Benin (UNIBEN)"),
        ("abu", "Ahmadu Bello University (ABU)"),
        ("unn", "University of Nigeria, Nsukka (UNN)"),
        ("lautech", "Ladoke Akintola University (LAUTECH)"),
        ("covenant", "Covenant University"),
        ("babcock", "Babcock University"),
        ("futa", "Federal University of Technology, Akure (FUTA)"),
        ("futo", "Federal University of Technology, Owerri (FUTO)"),
        ("lasu", "Lagos State University (LASU)"),
        ("eksu", "Ekiti State University (EKSU)"),
        ("other", "Other Institution"),
    ]
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    account_type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default="student",
    )
    
    # Student-specific fields
    school = models.CharField(
        max_length=50,
        choices=NIGERIAN_UNIVERSITIES,
        blank=True,
    )
    department = models.CharField(max_length=200, blank=True)
    bio = models.TextField(
        max_length=1000,
        blank=True,
        help_text="Tell clients about yourself, your skills and experience",
    )
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        help_text="WhatsApp number with country code (e.g., 2348012345678)",
    )
    skills = models.ManyToManyField(Skill, blank=True, related_name="users")
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        help_text="Upload a professional photo",
    )
    availability_status = models.CharField(
        max_length=15,
        choices=AVAILABILITY_CHOICES,
        default="available",
    )
    
    # Verification
    verified = models.BooleanField(default=False)
    verification_doc = models.ImageField(
        upload_to="verification/",
        blank=True,
        null=True,
        help_text="Upload student ID card for verification",
    )
    verification_date = models.DateTimeField(blank=True, null=True)
    
    # Profile completion tracking
    profile_complete = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Saved freelancers (for clients)
    saved_freelancers = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="saved_by",
    )
    
    # Dark mode preference
    dark_mode = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return self.full_name or self.username or self.email
    
    def get_absolute_url(self):
        return reverse("freelancer_detail", kwargs={"username": self.username})
    
    @property
    def whatsapp_link(self):
        """Generate WhatsApp click-to-chat link."""
        if self.whatsapp:
            from django.conf import settings
            message = getattr(settings, "WHATSAPP_DEFAULT_MESSAGE", "Hi! I found you on SkillPlug.")
            return f"https://wa.me/{self.whatsapp}?text={message.replace(' ', '%20')}"
        return ""
    
    @property
    def display_name(self):
        """Return the best available name for display."""
        return self.full_name or self.username or self.email.split("@")[0]
    
    @property
    def is_student(self):
        return self.account_type in ["student", "both"]
    
    @property
    def school_display(self):
        """Return the human-readable school name."""
        for code, name in self.NIGERIAN_UNIVERSITIES:
            if code == self.school:
                return name
        return self.school or "Not specified"
