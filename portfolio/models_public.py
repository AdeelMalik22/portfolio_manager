from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class UserProfile(models.Model):
    """Extended user profile for portfolio owners"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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
    """Live public portfolios (replaces downloadable portfolios)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='public_portfolio')
    username_slug = models.SlugField(unique=True, max_length=150)  # For URL: portfolios.com/username

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

    # Data (stored as JSON for flexibility)
    skills = models.JSONField(default=list)
    projects = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)

    # Template selection
    template = models.ForeignKey('PortfolioTemplate', on_delete=models.SET_NULL, null=True)

    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)  # For showcasing great portfolios
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

