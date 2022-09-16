from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from blog.views import PostHome

schema_view = get_schema_view(
   openapi.Info(
      title="KBLOG API",
      default_version='v1',
      description="Test blog",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="meigallo@meigallodixital.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', PostHome.as_view(), name="home" ),
    path('api/', PostHome.as_view(), name="home-api" ),
    # Admin routes
    path('admin/', admin.site.urls),
    # RF API auth
    path('api-auth/', include('rest_framework.urls')),
    # Accounts
    path('api/account/', include('account.urls')),
    # Blog routes
    path('api/blog/', include('blog.urls')),
    # JWT Auth
    path('api/account/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Doc
    re_path(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/doc', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
