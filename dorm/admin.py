from django.contrib import admin
from . import models

# Register your models here.
class RoomInline(admin.TabularInline):
    model = models.Room
    extra = 1

class BuildingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Info', {'fields': ['number', 'build_date', 'floor', 'volume', 'sex']})
    ]
    inlines = [RoomInline]
    list_display = ('number', 'floor', 'volume', 'sex')

admin.site.register(models.Building, BuildingAdmin)

class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'sex', 'info', 'number', 'idcard']}),
        ('Teacher Info', {'fields': ['teacher']}),
        ('Room Info', {'fields': ['room']})
    ]
    list_display = ('name', 'sex', 'idcard', 'info', 'number')

admin.site.register(models.Student, StudentAdmin)
