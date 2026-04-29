from django.contrib import admin
from .models import (
    PortfolioTemplate, Portfolio, PortfolioProject,
    PortfolioExperience, PortfolioEducation,
    UserProfile, PublicPortfolio
)


@admin.register(PortfolioTemplate)
class PortfolioTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'color_scheme', 'is_active', 'order')
    list_filter = ('category', 'is_active','id')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


class PortfolioProjectInline(admin.TabularInline):
    model = PortfolioProject
    extra = 0


class PortfolioExperienceInline(admin.TabularInline):
    model = PortfolioExperience
    extra = 0


class PortfolioEducationInline(admin.TabularInline):
    model = PortfolioEducation
    extra = 0


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'template', 'email', 'is_published', 'created_at')
    list_filter = ('template', 'is_published', 'created_at')
    search_fields = ('full_name', 'email', 'title')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PortfolioProjectInline, PortfolioExperienceInline, PortfolioEducationInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'title', 'bio', 'email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('linkedin', 'github', 'portfolio_website', 'twitter')
        }),
        ('Portfolio Data', {
            'fields': ('profile_image', 'skills', 'projects', 'experience', 'education', 'template')
        }),
        ('Status', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'website')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PublicPortfolio)
class PublicPortfolioAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username_slug', 'template', 'is_published', 'is_featured', 'view_count')
    list_filter = ('is_published', 'is_featured', 'template')
    search_fields = ('full_name', 'username_slug', 'email')
    readonly_fields = ('created_at', 'updated_at', 'view_count')

