from django.contrib import admin

from .models import Key, License, Project, Sale


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['modify_time', 'name', 'slug']


class KeyAdmin(admin.ModelAdmin):
    list_display = ['modify_time', 'project', 'prefix']
    readonly_fields = ['project']


class LicenseAdmin(admin.ModelAdmin):
    list_display = ['modify_time', 'user', 'days']
    readonly_fields = [
        'key',
        'user',
        'code',
        'days',
    ]


class SaleAdmin(admin.ModelAdmin):
    list_display = ['modify_time', 'product_id', 'sale_id']
    search_fields = ['sale_id', 'product_id']
    list_filter = ['modify_time']
    readonly_fields = [
        'create_time',
        'modify_time',
        'product_id',
        'sale_id',
        'license',
        'payload',
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Sale, SaleAdmin)
