from django.contrib import admin
from .models import DocType, DocField, DocPerm

class DocFieldInline(admin.TabularInline):
    model = DocField
    extra = 0

class DocPermInline(admin.TabularInline):
    model = DocPerm
    extra = 0

@admin.register(DocType)
class DocTypeAdmin(admin.ModelAdmin):
    list_display = ("name","label","module","modified")
    search_fields = ("name","label","module")
    inlines = [DocFieldInline, DocPermInline]

admin.site.register(DocField)
admin.site.register(DocPerm)
