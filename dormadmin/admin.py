from django.contrib import admin
from .models import DormAdminUser

# Register your models here.
class DormAdminUserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'sex', 'phone', 'idcard']}),
        ('Permission', {'fields': ['permission', 'workid', 'incharge']})
    ]
    list_display = ('name', 'sex', 'idcard', 'workid', 'permission', 'incharge',)

admin.site.register(DormAdminUser, DormAdminUserAdmin)
