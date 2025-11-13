from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Farqla API",
        default_version="v1",
        description="Bank xizmatlarini solishtirish tizimi (Farqla)",
        contact=openapi.Contact(email="support@itcomfort.uz"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/mobileapp/", include("apps.mobilapp.urls")),
    path("api/provayderapp/", include("apps.provayderapp.urls")),
    path("api/sugurtaapp/", include("apps.sugurtaapp.urls")),
    path("api/bankapp/", include("apps.bankapp.urls")),
    path("api/users/", include("apps.userapp.urls")),
    path("api/talimapp/", include("apps.talimapp.urls")),
    # Standart UI'lar
    re_path(r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),

    # 🔥 Dark Swagger (custom template)
    path("swagger-dark/", TemplateView.as_view(template_name="swagger_dark.html"), name="swagger-dark"),

    path("", RedirectView.as_view(url="/swagger/", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
