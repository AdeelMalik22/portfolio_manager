from django.db import models
from django.core.validators import URLValidator
from django.utils.text import slugify
from django.contrib.auth.models import User
import json

class PortfolioTemplate(models.Model):
    """Portfolio template model"""

    CATEGORY_CHOICES = [
        ('minimalist', 'Minimalist'),
        ('developer', 'Developer-Focused'),
        ('creative', 'Creative/Designer'),
        ('corporate', 'Corporate/Professional'),
        ('latest', 'Latest'),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    color_scheme = models.CharField(max_length=50, default='blue')
    template_file = models.CharField(max_length=200)  # Path to template HTML
    preview_image = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    """User portfolio data model"""

    # Basic Info
    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    # Social Links
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio_website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    # Profile Image
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    # Processed Profile Image (background removed + themed)
    processed_profile_image = models.ImageField(upload_to='profiles_processed/', null=True, blank=True)

    # Skills (stored as JSON)
    skills = models.JSONField(default=list)  # ["Python", "Django", "React"]

    # Template Selection
    template = models.ForeignKey(PortfolioTemplate, on_delete=models.PROTECT)

    # Additional Data (JSON for flexibility)
    projects = models.JSONField(default=list)  # List of project objects
    experience = models.JSONField(default=list)  # List of experience objects
    education = models.JSONField(default=list)  # List of education objects

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.template.name}"


class PortfolioProject(models.Model):
    """Nested project data (optional, for structured storage)"""

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='project_list')
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500)  # Comma-separated
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.portfolio.full_name} - {self.title}"


class PortfolioExperience(models.Model):
    """Nested experience data (optional)"""

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='experience_list')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)  # e.g., "Jan 2020 - Dec 2021"
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.portfolio.full_name} - {self.company}"


class PortfolioEducation(models.Model):
    """Nested education data (optional)"""

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='education_list')
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    year = models.CharField(max_length=20)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.portfolio.full_name} - {self.degree}"


class UserProfile(models.Model):
    """Extended user profile for portfolio owners"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio_profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portfolio_user_profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} Profile"


class PublicPortfolio(models.Model):
    """Live public portfolios (new model for live editing)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='public_portfolio')
    username_slug = models.SlugField(unique=True, max_length=150)

    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True)

    # Social links
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    portfolio_website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    # Media
    profile_image = models.ImageField(upload_to='portfolio_profiles/', null=True, blank=True)

    # Processed Profile Image (background removed + themed)
    processed_profile_image = models.ImageField(upload_to='portfolio_profiles_processed/', null=True, blank=True)

    # Data (stored as JSON for flexibility)
    skills = models.JSONField(default=list)
    projects = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)

    # Template selection
    template = models.ForeignKey(PortfolioTemplate, on_delete=models.SET_NULL, null=True)

    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portfolio_public_portfolio'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['username_slug']),
            models.Index(fields=['is_published', 'is_featured']),
        ]

    def save(self, *args, **kwargs):
        if not self.username_slug:
            self.username_slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name}'s Portfolio"

    @property
    def public_url(self):
        """Generate public URL for this portfolio"""
        return f"/portfolio/{self.username_slug}/"
