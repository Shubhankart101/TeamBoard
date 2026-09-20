from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from .views import register_view, login_view, query_kb_view, usage_summary_view

urlpatterns = [
    # OpenAPI Schema & Swagger Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui-alias'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API Endpoints
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('kb/query/', query_kb_view, name='query_kb'),
    path('admin/usage-summary/', usage_summary_view, name='usage_summary'),
]
