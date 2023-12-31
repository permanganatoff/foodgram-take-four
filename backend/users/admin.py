from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class UserAdmin(UserAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'display_recipes_count',
        'display_subscribers_count',
        'is_active',
        'id'
    )
    list_filter = ('email', 'first_name', 'is_active')
    search_fields = ('username', 'email')

    @admin.display(description='Count of recipes')
    def display_recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description='Count of subscribers')
    def display_subscribers_count(self, obj):
        return obj.author.count()


admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
