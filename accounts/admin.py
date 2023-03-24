from django.contrib import admin

from .models import FriendShip, User


class UserAdmin(admin.ModelAdmin):
    fields = ["email", "username"]


admin.site.register(User, UserAdmin)
admin.site.register(FriendShip)
