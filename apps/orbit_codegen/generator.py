from apps.orbit_core.models import DocType
from django.utils.text import slugify
from pathlib import Path

ALLOWED = {"Data","Text","LongText","Int","Float","Currency","Check","Date","DateTime","Select","Link","Table","Attach","AttachImage"}

def generate_model(dt: DocType):
    for f in dt.field_set.all():
        if f.type not in ALLOWED:
            raise ValueError(f"Unsupported: {f.type}")
        if f.type == "Link" and not f.link_to:
            raise ValueError(f"{f.fieldname}: link_to required")
        if f.type == "Table" and not f.table_doctype:
            raise ValueError(f"{f.fieldname}: table_doctype required")

    app_dir = Path("apps")/dt.module.lower()
    app_dir.mkdir(parents=True, exist_ok=True)
    (app_dir/"__init__.py").touch()

    fields_py = []
    for f in dt.field_set.order_by("idx"):
        map_py = {
            "Data":"models.CharField(max_length=255, null=True, blank=True)",
            "Text":"models.TextField(null=True, blank=True)",
            "LongText":"models.TextField(null=True, blank=True)",
            "Int":"models.IntegerField(null=True, blank=True)",
            "Float":"models.FloatField(null=True, blank=True)",
            "Currency":"models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)",
            "Check":"models.BooleanField(default=False)",
            "Date":"models.DateField(null=True, blank=True)",
            "DateTime":"models.DateTimeField(null=True, blank=True)",
            "Select":"models.CharField(max_length=120, null=True, blank=True)",
            "Link":f"models.ForeignKey('{f.link_to}', on_delete=models.PROTECT, null=True, blank=True)",
            "Table":"models.JSONField(default=list, blank=True)",
            "Attach":"models.CharField(max_length=255, null=True, blank=True)",
            "AttachImage":"models.CharField(max_length=255, null=True, blank=True)",
        }
        py = f"    {f.fieldname} = {map_py[f.type]}"
        if f.unique: py = py.replace(")", ", unique=True)")
        if f.index:  py = py.replace(")", ", db_index=True)")
        fields_py.append(py)

    src = f'''from django.db import models
class {dt.name}(models.Model):
{"".join(line + "\\n" for line in fields_py)}    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    def __str__(self): return getattr(self, "{dt.title_field or 'id'}", str(self.id))
'''
    with open(app_dir/f"models_{slugify(dt.name)}.py","w",encoding="utf-8") as fh:
        fh.write(src)
    print(f"[orbit] Generated: apps/{dt.module.lower()}/models_{slugify(dt.name)}.py")
