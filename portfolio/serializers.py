from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    PortfolioTemplate, Portfolio, PortfolioProject,
    PortfolioExperience, PortfolioEducation, UserProfile, PublicPortfolio
)


class PortfolioTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioTemplate
        fields = ['id', 'name', 'slug', 'description', 'category',
                  'color_scheme', 'template_file', 'preview_image', 'is_active']


class PortfolioTemplateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioTemplate
        fields = '__all__'


class PortfolioProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioProject
        fields = ['id', 'title', 'description', 'tech_stack', 'github_link', 'live_link', 'order']


class PortfolioExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioExperience
        fields = ['id', 'company', 'role', 'duration', 'description', 'order']


class PortfolioEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioEducation
        fields = ['id', 'school', 'degree', 'field', 'year']


class PortfolioSerializer(serializers.ModelSerializer):
    project_list = PortfolioProjectSerializer(many=True, read_only=True)
    experience_list = PortfolioExperienceSerializer(many=True, read_only=True)
    education_list = PortfolioEducationSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            'id', 'full_name', 'title', 'bio', 'email', 'phone', 'location',
            'linkedin', 'github', 'portfolio_website', 'twitter',
            'profile_image', 'skills', 'template', 'projects', 'experience',
            'education', 'project_list', 'experience_list', 'education_list',
            'created_at', 'updated_at', 'is_published'
        ]
        read_only_fields = ['created_at', 'updated_at']


class PortfolioCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = [
            'id', 'full_name', 'title', 'bio', 'email', 'phone', 'location',
            'linkedin', 'github', 'portfolio_website', 'twitter',
            'profile_image', 'skills', 'template', 'projects',
            'experience', 'education'
        ]
        read_only_fields = ['id']


# Authentication Serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'bio', 'avatar', 'website', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        # Create UserProfile
        UserProfile.objects.create(user=user)
        # Create PublicPortfolio
        PublicPortfolio.objects.create(
            user=user,
            username_slug=user.username,
            full_name=f"{user.first_name} {user.last_name}".strip() or user.username,
            title="",
            bio="",
            email=user.email,
        )
        return user


class PublicPortfolioSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    template_slug = serializers.CharField(source='template.slug', read_only=True)

    class Meta:
        model = PublicPortfolio
        fields = [
            'id', 'username_slug', 'full_name', 'title', 'bio', 'email', 'phone', 'location',
            'linkedin', 'github', 'portfolio_website', 'twitter', 'profile_image',
            'skills', 'projects', 'experience', 'education', 'template', 'template_name',
            'template_slug', 'is_published', 'is_featured', 'view_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['username_slug', 'view_count', 'created_at', 'updated_at']


class PublicPortfolioEditSerializer(serializers.ModelSerializer):
    """Serializer for editing own public portfolio (authenticated users)"""

    class Meta:
        model = PublicPortfolio
        fields = [
            'full_name', 'title', 'bio', 'email', 'phone', 'location',
            'linkedin', 'github', 'portfolio_website', 'twitter', 'profile_image',
            'skills', 'projects', 'experience', 'education', 'template', 'is_published'
        ]

