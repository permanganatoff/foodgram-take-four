from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Subscription, User


@admin.register(User)
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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author', 'id')
    list_filter = ('user', 'author', 'id')
    search_fields = ('user', 'author', 'id')
