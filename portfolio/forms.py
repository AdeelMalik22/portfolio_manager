from django import forms
from .models import PublicPortfolio


class PublicPortfolioForm(forms.ModelForm):
    skills = forms.JSONField(required=False)
    projects = forms.JSONField(required=False)
    experience = forms.JSONField(required=False)
    education = forms.JSONField(required=False)

    class Meta:
        model = PublicPortfolio
        fields = [
            'full_name', 'title', 'bio', 'email', 'phone', 'location',
            'linkedin', 'github', 'portfolio_website', 'twitter',
            'profile_image', 'skills', 'projects', 'experience', 'education',
            'template', 'is_published'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'projects': forms.Textarea(attrs={'rows': 5}),
            'experience': forms.Textarea(attrs={'rows': 5}),
            'education': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned = super().clean()
        for field in ['skills', 'projects', 'experience', 'education']:
            if cleaned.get(field) in [None, '']:
                cleaned[field] = []
        return cleaned

