from django.contrib import admin

# Register your models here.
from .models import (
    Requests,
    ReqSpec,
    Xpref,
    PrefSpec,
    Payment,
    ProjectType,
    FrameSize,
    IPType, ICType, IMType)

admin.site.register(Requests)
admin.site.register(ReqSpec)
admin.site.register(Xpref)
admin.site.register(PrefSpec)
admin.site.register(Payment)
admin.site.register(ProjectType)
admin.site.register(IPType)
admin.site.register(ICType)
admin.site.register(IMType)
admin.site.register(FrameSize)