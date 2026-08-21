from django.contrib import admin
from .models import Architecture,ArchitectureType,UserArchitecture,Technology,TechnologyCategory,ProjectField

admin.site.register(ArchitectureType)
admin.site.register(Architecture)
admin.site.register(UserArchitecture)
admin.site.register(TechnologyCategory)
admin.site.register(Technology)
admin.site.register(ProjectField)
