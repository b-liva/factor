from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import MotorsCode
from import_export import resources

# Register your models here.

@admin.register(MotorsCode)
# admin.site.register(MotorsCode)

class MotorsCodeAdmin(ImportExportModelAdmin):
    pass

