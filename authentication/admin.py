from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']

admin.site.register(User,UserAdmin)