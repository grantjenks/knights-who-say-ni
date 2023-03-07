from django.contrib import admin
from .models import Project, Key, License


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['modify_time', 'name', 'slug']


class KeyAdmin(admin.ModelAdmin):
    list_display = ['modify_time', 'project', 'prefix']


class LicenseAdmin(admin.ModelAdmin):
    list_display = ['modify_time', 'user', 'days']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(License, LicenseAdmin)
