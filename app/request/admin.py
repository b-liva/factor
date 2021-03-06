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
    IssueType,
    ProformaFollowUP,
    RpmType, IPType, ICType, IMType, IEType, Comment, PaymentType,
    Perm,
    PermSpec,
    InventoryOut,
    InventoryOutSpec,
    Invoice,
    InvoiceSpec,
    ProfChangeRequest
)

admin.site.register(Requests)
admin.site.register(ReqSpec)
admin.site.register(Xpref)
admin.site.register(PrefSpec)
admin.site.register(Payment)
admin.site.register(PaymentType)
admin.site.register(Comment)
admin.site.register(ProjectType)
admin.site.register(RpmType)
admin.site.register(IPType)
admin.site.register(ICType)
admin.site.register(IMType)
admin.site.register(IEType)
admin.site.register(FrameSize)
admin.site.register(IssueType)
admin.site.register(ProformaFollowUP)
admin.site.register(Perm)
admin.site.register(PermSpec)
admin.site.register(InventoryOut)
admin.site.register(InventoryOutSpec)
admin.site.register(Invoice)
admin.site.register(InvoiceSpec)
admin.site.register(ProfChangeRequest)