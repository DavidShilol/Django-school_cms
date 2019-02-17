from django.contrib import admin
from .models import TeacherUser

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'sex', 'phone', 'idcard', 'workid']})
    ]
    list_display = ('name', 'sex', 'idcard', 'workid')

admin.site.register(TeacherUser, TeacherAdmin)

