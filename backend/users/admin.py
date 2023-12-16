from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class UserAdmin(UserAdmin):
    list_display = (
        "username",
        "id",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "get_recipes_count",
        "get_subscribers_count",
    )
    list_filter = ("email", "first_name", "is_active")
    search_fields = (
        "username",
        "email",
    )
    empty_value_display = "-empty-"

    save_on_top = True

    @admin.display(description="Количество рецептов")
    def get_recipes_count(self, obj):
        return obj.recipes.count()

    @admin.display(description="Количество подписчиков")
    def get_subscribers_count(self, obj):
        return obj.author.count()


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "author")
    search_fields = ("user", "author")
    list_filter = ("user", "author")
    empty_value_display = "-empty-"

    save_on_top = True


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
