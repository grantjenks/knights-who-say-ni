from django.contrib import admin
from .models import Project, Key, License


class ProjectAdmin(admin.ModelAdmin):
    pass


class KeyAdmin(admin.ModelAdmin):
    pass


class LicenseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(License, LicenseAdmin)
