from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponseRedirect
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .viewsets import register_doctype_viewsets

router = DefaultRouter()
try:
    register_doctype_viewsets(router)
except Exception:
    pass

def root_redirect(_request):
    return HttpResponseRedirect("/schema/")

urlpatterns = [
    path("", root_redirect),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("schema.yaml", SpectacularAPIView.as_view(), name="schema"),
    path("schema/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
