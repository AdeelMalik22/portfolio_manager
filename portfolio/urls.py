from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'portfolio'

router = DefaultRouter()
router.register(r'templates', views.PortfolioTemplateViewSet, basename='template')
router.register(r'portfolios', views.PortfolioViewSet, basename='portfolio')

urlpatterns = [
    path('', include(router.urls)),
    path('template/<int:template_id>/preview/', views.template_preview, name='template_preview'),
    path('auth/register/', views.register, name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('auth/logout/', views.logout, name='auth_logout'),
    path('auth/profile/', views.my_profile, name='auth_profile'),
    path('portfolios/featured/', views.featured_portfolios, name='featured_portfolios'),
    path('my-portfolio/', views.my_portfolio, name='my_portfolio'),
    path('my-portfolio/publish/', views.publish_my_portfolio, name='my_portfolio_publish'),
    path('my-portfolio/unpublish/', views.unpublish_my_portfolio, name='my_portfolio_unpublish'),
    path('my-portfolio/process-image/', views.process_my_portfolio_image, name='my_portfolio_process_image'),
]

# Web URLs (non-API)
web_urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery, name='gallery'),
    path('form/', views.portfolio_form, name='portfolio_form'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/edit/', views.dashboard_edit, name='dashboard_edit'),
    path('portfolio/<slug:username_slug>/', views.public_portfolio_view, name='public_portfolio_view'),
]

