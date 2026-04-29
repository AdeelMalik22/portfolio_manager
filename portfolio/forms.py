from django import forms
from .models import PublicPortfolio


class PublicPortfolioForm(forms.ModelForm):
    skills = forms.JSONField(required=False)
    projects = forms.JSONField(required=False)
    experience = forms.JSONField(required=False)
    education = forms.JSONField(required=False)

    # Option to auto-process image
    auto_process_image = forms.BooleanField(required=False, initial=True)

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
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def clean(self):
        cleaned = super().clean()
        for field in ['skills', 'projects', 'experience', 'education']:
            if cleaned.get(field) in [None, '']:
                cleaned[field] = []
        return cleaned

    def save(self, commit=True):
        """Override save to process image if requested"""
        instance = super().save(commit=commit)

        # Process image if auto_process_image is checked and image exists
        if self.cleaned_data.get('auto_process_image') and self.files.get('profile_image'):
            try:
                from .image_processor import ImageProcessor
                processor = ImageProcessor()
                template_slug = instance.template.slug if instance.template else 'modern_corporate'
                processed_file = processor.save_processed_image(
                    self.files['profile_image'],
                    template_slug
                )
                instance.processed_profile_image = processed_file
                if commit:
                    instance.save()
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed to auto-process image: {e}")

        return instance


