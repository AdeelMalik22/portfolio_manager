from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
import json

from .models import PortfolioTemplate, Portfolio, UserProfile, PublicPortfolio
from .serializers import (
    PortfolioTemplateSerializer, PortfolioTemplateDetailSerializer,
    PortfolioSerializer, PortfolioCreateUpdateSerializer,
    UserRegistrationSerializer, UserProfileSerializer,
    PublicPortfolioSerializer, PublicPortfolioEditSerializer
)
from .services import PortfolioRenderer, PublicPortfolioRenderer
from .image_processor import ImageProcessor
from .forms import PublicPortfolioForm
from .preview_context import (
    PreviewPayloadError,
    build_draft_preview_context,
    build_sample_preview_context,
)


class PortfolioTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for portfolio templates"""
    queryset = PortfolioTemplate.objects.filter(is_active=True)
    serializer_class = PortfolioTemplateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['order', 'name', 'category']
    ordering = ['order', 'name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PortfolioTemplateDetailSerializer
        return PortfolioTemplateSerializer

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get templates by category"""
        category = request.query_params.get('category', None)
        if category:
            templates = self.queryset.filter(category=category)
        else:
            templates = self.queryset

        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)


class PortfolioViewSet(viewsets.ModelViewSet):
    """ViewSet for user portfolios"""
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'email', 'title']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['-created_at']
    permission_classes = [AllowAny]  # Allow unauthenticated portfolio creation

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PortfolioCreateUpdateSerializer
        return PortfolioSerializer

    def create(self, request, *args, **kwargs):
        """Create a new portfolio"""
        # Handle form data
        data = request.data.dict() if hasattr(request.data, 'dict') else dict(request.data)

        # Parse JSON fields
        if 'skills' in data and isinstance(data['skills'], str):
            try:
                data['skills'] = json.loads(data['skills'])
            except:
                data['skills'] = data['skills'].split(',')

        if 'projects' in data and isinstance(data['projects'], str):
            try:
                data['projects'] = json.loads(data['projects'])
            except:
                data['projects'] = []

        if 'experience' in data and isinstance(data['experience'], str):
            try:
                data['experience'] = json.loads(data['experience'])
            except:
                data['experience'] = []

        if 'education' in data and isinstance(data['education'], str):
            try:
                data['education'] = json.loads(data['education'])
            except:
                data['education'] = []

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """Preview portfolio with selected template"""
        portfolio = self.get_object()
        renderer = PortfolioRenderer(portfolio)
        html = renderer.render_html()
        return HttpResponse(html, content_type='text/html')

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download portfolio as HTML file"""
        portfolio = self.get_object()
        renderer = PortfolioRenderer(portfolio)
        html = renderer.render_html()
        filename = renderer.get_filename()

        response = HttpResponse(html, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish portfolio"""
        portfolio = self.get_object()
        portfolio.is_published = True
        portfolio.save()
        serializer = self.get_serializer(portfolio)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """Unpublish portfolio"""
        portfolio = self.get_object()
        portfolio.is_published = False
        portfolio.save()
        serializer = self.get_serializer(portfolio)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], parser_classes=(MultiPartParser, FormParser))
    def process_image(self, request, pk=None):
        """Process profile image: remove background and merge with template theme"""
        portfolio = self.get_object()
        
        # Get image file
        image_file = request.FILES.get('image')
        if not image_file:
            return Response(
                {'error': 'No image file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get template slug
        template_slug = request.data.get('template_slug', portfolio.template.slug)
        
        try:
            # Process image
            processor = ImageProcessor()
            processed_file = processor.save_processed_image(image_file, template_slug)
            
            # Save to portfolio
            portfolio.processed_profile_image = processed_file
            portfolio.save(update_fields=['processed_profile_image'])
            
            serializer = self.get_serializer(portfolio)
            return Response({
                'message': 'Image processed successfully',
                'portfolio': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Image processing failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


# Regular views for template preview
@xframe_options_sameorigin
@require_http_methods(["GET", "POST"])
def template_preview(request, template_id):
    """Render either a rich public sample or an unsaved private form draft."""
    template = get_object_or_404(PortfolioTemplate, id=template_id, is_active=True)

    if request.method == "POST":
        try:
            context = build_draft_preview_context(
                template,
                request.POST,
                request.FILES.get("profile_image"),
            )
        except PreviewPayloadError as exc:
            response = HttpResponse(str(exc), status=400, content_type="text/plain; charset=utf-8")
            response["Cache-Control"] = "no-store"
            return response
    else:
        context = build_sample_preview_context(template)

    response = HttpResponse(
        render_to_string(template.template_file, context),
        content_type="text/html; charset=utf-8",
    )
    # Draft data and uploaded images are rendered only for the requesting user.
    response["Cache-Control"] = "no-store"
    return response


def index(request):
    """Homepage view"""
    active_templates = PortfolioTemplate.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'index.html', {
        'template_count': active_templates.count(),
        'featured_templates': active_templates[:3],
    })


def gallery(request):
    """Template gallery view — passes per-category counts to the template"""
    templates = PortfolioTemplate.objects.filter(is_active=True).order_by('category', 'order', 'name')
    active_qs = PortfolioTemplate.objects.filter(is_active=True)
    category_counts = {
        'all':        active_qs.count(),
        'minimalist': active_qs.filter(category='minimalist').count(),
        'developer':  active_qs.filter(category='developer').count(),
        'creative':   active_qs.filter(category='creative').count(),
        'corporate':  active_qs.filter(category='corporate').count(),
    }
    return render(request, 'portfolio_gallery.html', {
        'templates': templates,
        'category_counts': category_counts,
    })


def portfolio_form(request):
    """Portfolio builder form view"""
    templates = PortfolioTemplate.objects.filter(is_active=True).order_by('order')
    return render(request, 'portfolio_form.html', {'templates': templates})


# Authentication and user profile APIs

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user and return JWT tokens"""
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        },
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Stateless logout endpoint for JWT clients"""
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    """Get or update the authenticated user's profile"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# Public portfolio APIs

@api_view(['GET'])
@permission_classes([AllowAny])
def featured_portfolios(request):
    """List featured, published public portfolios"""
    portfolios = PublicPortfolio.objects.filter(is_published=True, is_featured=True).order_by('-updated_at')
    serializer = PublicPortfolioSerializer(portfolios, many=True)
    return Response(serializer.data)


# Authenticated portfolio APIs

def _get_or_create_public_portfolio(user):
    defaults = {
        'username_slug': user.username,
        'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
        'title': '',
        'bio': '',
        'email': user.email or '',
    }
    portfolio, _ = PublicPortfolio.objects.get_or_create(user=user, defaults=defaults)
    return portfolio


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_portfolio(request):
    """Get or update the authenticated user's public portfolio"""
    portfolio = _get_or_create_public_portfolio(request.user)

    if request.method == 'GET':
        serializer = PublicPortfolioSerializer(portfolio)
        return Response(serializer.data)

    serializer = PublicPortfolioEditSerializer(portfolio, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(PublicPortfolioSerializer(portfolio).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_my_portfolio(request):
    """Publish the authenticated user's public portfolio"""
    portfolio = _get_or_create_public_portfolio(request.user)
    portfolio.is_published = True
    portfolio.save(update_fields=['is_published'])
    return Response(PublicPortfolioSerializer(portfolio).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unpublish_my_portfolio(request):
    """Unpublish the authenticated user's public portfolio"""
    portfolio = _get_or_create_public_portfolio(request.user)
    portfolio.is_published = False
    portfolio.save(update_fields=['is_published'])
    return Response(PublicPortfolioSerializer(portfolio).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_my_portfolio_image(request):
    """Process profile image for authenticated user's public portfolio"""
    portfolio = _get_or_create_public_portfolio(request.user)
    
    # Get image file
    image_file = request.FILES.get('image')
    if not image_file:
        return Response(
            {'error': 'No image file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Get template slug
    template_slug = request.data.get('template_slug')
    if not template_slug and portfolio.template:
        template_slug = portfolio.template.slug
    else:
        template_slug = template_slug or 'modern_corporate'
    
    try:
        # Process image
        processor = ImageProcessor()
        processed_file = processor.save_processed_image(image_file, template_slug)
        
        # Save to portfolio
        portfolio.processed_profile_image = processed_file
        portfolio.save(update_fields=['processed_profile_image'])
        
        return Response({
            'message': 'Image processed successfully',
            'portfolio': PublicPortfolioSerializer(portfolio).data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Image processing failed: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


# Public portfolio HTML rendering

def public_portfolio_view(request, username_slug):
    """Render a published public portfolio using its selected template"""
    portfolio = get_object_or_404(PublicPortfolio, username_slug=username_slug, is_published=True)

    if not portfolio.template:
        fallback_template = PortfolioTemplate.objects.filter(is_active=True).order_by('order').first()
        if not fallback_template:
            return HttpResponse('No templates available.', status=404)
        portfolio.template = fallback_template
        portfolio.save(update_fields=['template'])

    PublicPortfolio.objects.filter(id=portfolio.id).update(view_count=F('view_count') + 1)
    portfolio.refresh_from_db(fields=['view_count'])

    renderer = PublicPortfolioRenderer(portfolio)
    html = renderer.render_html()
    return HttpResponse(html, content_type='text/html')


# Dashboard views (session-authenticated)

@login_required
def dashboard(request):
    """Simple dashboard for managing a public portfolio"""
    portfolio = _get_or_create_public_portfolio(request.user)
    return render(request, 'dashboard.html', {
        'portfolio': portfolio,
    })


@login_required
def dashboard_edit(request):
    """Edit public portfolio details from the dashboard"""
    portfolio = _get_or_create_public_portfolio(request.user)

    if request.method == 'POST':
        form = PublicPortfolioForm(request.POST, request.FILES, instance=portfolio)
        if form.is_valid():
            form.save()
            return redirect('portfolio:dashboard')
    else:
        form = PublicPortfolioForm(instance=portfolio)

    return render(request, 'portfolio_edit.html', {
        'form': form,
        'portfolio': portfolio,
    })
