from rest_framework import viewsets, filters, serializers
from django.apps import apps

def build_serializer(model):
    class _S(serializers.ModelSerializer):
        class Meta:
            model = model
            fields = "__all__"
    return _S

def build_viewset(model, search_fields=None, ordering="id"):
    class _V(viewsets.ModelViewSet):
        queryset = model.objects.all()
        serializer_class = build_serializer(model)
        filter_backends = [filters.SearchFilter, filters.OrderingFilter]
        search_fields = search_fields or []
        ordering = (ordering,)
    return _V

def register_doctype_viewsets(router):
    try:
        DocType = apps.get_model("orbit_core","DocType")
    except Exception:
        return
    for dt in DocType.objects.all():
        try:
            model = apps.get_model(dt.module.lower(), dt.name)
        except Exception:
            continue
        vs = build_viewset(model, dt.search_field_list(), dt.sort_by)
        router.register(dt.name.lower(), vs, basename=dt.name.lower())
