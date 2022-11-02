from django.contrib import admin

from account.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active', 'is_staff')
    list_editable = ('is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    list_display_links = ('email', 'username')
    fields = ('email', 'username', 'password', 'is_active', 'is_staff')
    search_fields = ('emails', 'username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'are_results_shown', 'is_email_shown')
    list_editable = ('are_results_shown', 'is_email_shown')
    list_filter = ('are_results_shown', 'is_email_shown')
