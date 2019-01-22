from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import ReqEntered
from import_export import resources

# Register your models here.
# admin.site.register(ReqEntered)
@admin.register(ReqEntered)

# class ReqResource(resources.ModelResource):
#
#     class Meta:
#         model = ReqEntered

class ReqAdmin(ImportExportModelAdmin):
    pass

