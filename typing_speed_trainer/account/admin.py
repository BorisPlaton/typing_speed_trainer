from django.contrib import admin

from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active', 'is_staff',)
    list_editable = ('is_active', 'is_staff',)

    fields = ('email', 'username', 'is_active', 'is_staff',)
    search_fields = ('emails', 'username',)
