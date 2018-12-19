from django.contrib import admin

# Register your models here.
from .models import Requests
from .models import ProjectType
from .models import FrameSize
from .models import Prefactor
from .models import PrefactorVerification

admin.site.register(Requests)
admin.site.register(ProjectType)
admin.site.register(FrameSize)
admin.site.register(Prefactor)
admin.site.register(PrefactorVerification)