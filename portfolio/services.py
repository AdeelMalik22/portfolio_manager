"""
Portfolio rendering service - generates downloadable HTML portfolios
"""
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from io import BytesIO
import base64
import mimetypes
from pathlib import Path


class PortfolioRenderer:
    """Service to render portfolio templates with user data"""

    def __init__(self, portfolio):
        """Initialize with portfolio instance"""
        self.portfolio = portfolio
        self.template_path = portfolio.template.template_file

    def encode_image_to_base64(self):
        """Convert profile image to base64 for embedding in HTML"""
        # Use processed image if available, otherwise use original
        image_to_use = self.portfolio.processed_profile_image or self.portfolio.profile_image

        if not image_to_use:
            return None

        try:
            with image_to_use.open('rb') as f:
                image_data = f.read()
                base64_str = base64.b64encode(image_data).decode('utf-8')
                mime_type = mimetypes.guess_type(image_to_use.name)[0] or 'image/jpeg'
                return f"data:{mime_type};base64,{base64_str}"
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None

    def get_context_data(self):
        """Build context data for template rendering"""
        context = {
            'portfolio': self.portfolio,
            'full_name': self.portfolio.full_name,
            'title': self.portfolio.title,
            'bio': self.portfolio.bio,
            'email': self.portfolio.email,
            'phone': self.portfolio.phone,
            'location': self.portfolio.location,
            'linkedin': self.portfolio.linkedin,
            'github': self.portfolio.github,
            'portfolio_website': self.portfolio.portfolio_website,
            'twitter': self.portfolio.twitter,
            'skills': self.portfolio.skills,
            'projects': self.portfolio.projects,
            'experience': self.portfolio.experience,
            'education': self.portfolio.education,
            'profile_image_base64': self.encode_image_to_base64(),
            'template_color': self.portfolio.template.color_scheme,
        }
        return context

    def render_html(self):
        """Render the portfolio template to HTML string"""
        context = self.get_context_data()
        html = render_to_string(
            template_name=self.template_path,
            context=context,
            using='django'
        )
        return html

    def get_filename(self):
        """Generate filename for download"""
        # Remove spaces and special chars
        safe_name = self.portfolio.full_name.lower().replace(' ', '_')
        safe_name = ''.join(c for c in safe_name if c.isalnum() or c == '_')
        return f"{safe_name}_portfolio.html"


class PublicPortfolioRenderer:
    """Service to render public portfolio templates with user data"""

    def __init__(self, public_portfolio):
        """Initialize with PublicPortfolio instance"""
        self.portfolio = public_portfolio
        if not self.portfolio.template:
            raise ValueError("Public portfolio is missing a template")
        self.template_path = self.portfolio.template.template_file

    def encode_image_to_base64(self):
        """Convert profile image to base64 for embedding in HTML"""
        # Use processed image if available, otherwise use original
        image_to_use = self.portfolio.processed_profile_image or self.portfolio.profile_image

        if not image_to_use:
            return None

        try:
            with image_to_use.open('rb') as f:
                image_data = f.read()
                base64_str = base64.b64encode(image_data).decode('utf-8')
                mime_type = mimetypes.guess_type(image_to_use.name)[0] or 'image/jpeg'
                return f"data:{mime_type};base64,{base64_str}"
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None

    def get_context_data(self):
        """Build context data for template rendering"""
        context = {
            'portfolio': self.portfolio,
            'full_name': self.portfolio.full_name,
            'title': self.portfolio.title,
            'bio': self.portfolio.bio,
            'email': self.portfolio.email,
            'phone': self.portfolio.phone,
            'location': self.portfolio.location,
            'linkedin': self.portfolio.linkedin,
            'github': self.portfolio.github,
            'portfolio_website': self.portfolio.portfolio_website,
            'twitter': self.portfolio.twitter,
            'skills': self.portfolio.skills,
            'projects': self.portfolio.projects,
            'experience': self.portfolio.experience,
            'education': self.portfolio.education,
            'profile_image_base64': self.encode_image_to_base64(),
            'template_color': self.portfolio.template.color_scheme,
        }
        return context

    def render_html(self):
        """Render the portfolio template to HTML string"""
        context = self.get_context_data()
        html = render_to_string(
            template_name=self.template_path,
            context=context,
            using='django'
        )
        return html


