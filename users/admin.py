from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'is_active', 'role', 'is_staff',)
    list_display_links = ('email',)
    list_filter = ('is_staff', 'is_active',)
    search_fields = ('first_name', 'last_name', 'email',)
