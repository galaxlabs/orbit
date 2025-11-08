from django.db import models
from django.core.validators import RegexValidator

ROLE_NAME_VALIDATOR = RegexValidator(r"^[A-Za-z0-9 _.-]+$", "Invalid role")

class BaseStamped(models.Model):
    name = models.SlugField(max_length=160, unique=True)
    label = models.CharField(max_length=255)
    module = models.CharField(max_length=120, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta: abstract = True

class DocType(BaseStamped):
    is_single = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    is_tree = models.BooleanField(default=False)
    is_submittable = models.BooleanField(default=False)
    naming_rule = models.CharField(max_length=20, default="set_by_user",
        choices=[("set_by_user","set_by_user"),("autoincrement","autoincrement"),("series","series"),("field","field"),("format","format")])
    naming_series = models.CharField(max_length=120, null=True, blank=True)
    naming_field  = models.CharField(max_length=120, null=True, blank=True)
    naming_format = models.CharField(max_length=200, null=True, blank=True)
    title_field = models.CharField(max_length=120, null=True, blank=True)
    search_fields = models.CharField(max_length=400, null=True, blank=True)
    default_view = models.CharField(max_length=20, default="list")
    sort_by = models.CharField(max_length=120, default="modified")
    sort_order = models.CharField(max_length=4, default="DESC")
    icon = models.CharField(max_length=60, null=True, blank=True)
    color = models.CharField(max_length=40, null=True, blank=True)
    def search_field_list(self):
        return [s.strip() for s in (self.search_fields or "").split(",") if s.strip()]
    def __str__(self): return self.label or self.name

class DocField(models.Model):
    doctype = models.ForeignKey(DocType, related_name="field_set", on_delete=models.CASCADE)
    idx = models.PositiveIntegerField(default=0, db_index=True)
    fieldname = models.SlugField(max_length=160)
    label = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    required = models.BooleanField(default=False)
    unique = models.BooleanField(default=False)
    index = models.BooleanField(default=False)
    default = models.TextField(null=True, blank=True)
    options = models.TextField(null=True, blank=True)
    link_to = models.CharField(max_length=160, null=True, blank=True)
    table_doctype = models.CharField(max_length=160, null=True, blank=True)
    precision = models.IntegerField(null=True, blank=True)
    read_only = models.BooleanField(default=False)
    visible_roles = models.CharField(max_length=500, null=True, blank=True)
    class Meta:
        unique_together = ("doctype","fieldname")
        ordering = ["idx"]

class DocPerm(models.Model):
    doctype = models.ForeignKey(DocType, related_name="perm_set", on_delete=models.CASCADE)
    role = models.CharField(max_length=120, validators=[ROLE_NAME_VALIDATOR])
    read = models.BooleanField(default=True)
    create = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    submit = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    row_filter = models.TextField(null=True, blank=True)
    class Meta:
        unique_together = ("doctype","role")
