from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    fields = ["email", "username"]


admin.site.register(User, UserAdmin)
