from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Campaign, School, Manager


class ManagerInline(admin.StackedInline):
    model = Manager
    can_delete = False
    verbose_name_plural = 'manager'

class UserAdmin(BaseUserAdmin):
    inlines = (ManagerInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Campaign)
admin.site.register(School)

# Register your models here.
