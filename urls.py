from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from abcp_parser.views import abcp

schema_view = get_schema_view(
   openapi.Info(
      title="abcp_parse",
      default_version='v1',
      description="API работы с парсером abcp",
      terms_of_service=None,
      contact=openapi.Contact(email="shamemask@ya.ru"),
      license=None,
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
      path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
      path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
      path('abcp/', abcp, name='abcp'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)