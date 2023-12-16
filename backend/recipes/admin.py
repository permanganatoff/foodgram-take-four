from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from recipes.constants import MAX_INGREDIENTS

from .models import (AmountIngredient, Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)


class IngredientInline(admin.TabularInline):
    model = AmountIngredient
    extra = MAX_INGREDIENTS


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "author",
        "get_image",
        "cooking_time",
        "count_favorites",
        "get_ingredients",
    )
    fields = (
        (
            "name",
            "cooking_time",
        ),
        (
            "author",
            "tags",
        ),
        ("text",),
        ("image",),
    )
    raw_id_fields = ("author",)
    search_fields = (
        "name",
        "author__username",
        "tags__name",
    )
    list_filter = ("name", "author__username", "tags__name")

    inlines = (IngredientInline,)
    save_on_top = True
    empty_value_display = "-empty-"

    @admin.display(description="Photo")
    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='80' hieght='30'")

    @admin.display(description="In favorites")
    def count_favorites(self, obj):
        return obj.recipes_favorite_related.count()

    @admin.display(description="Ingredients")
    def get_ingredients(self, obj):
        return ", ".join(
            ingredient.name for ingredient in obj.ingredients.all())

    list_display_links = ("name", "author")


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-empty-"

    save_on_top = True


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )
    empty_value_display = "-empty-"
    search_fields = ("name", "color")
    list_display_links = ("name", "color")
    save_on_top = True


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )
    search_fields = ("user__username", "recipe__name")
    empty_value_display = "-empty-"
    list_display_links = ("user", "recipe")
    save_on_top = True


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
        "date_added",
    )
    search_fields = ("user__username", "recipe__name")
    empty_value_display = "-empty-"
    list_display_links = ("user", "recipe")
    save_on_top = True


class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "ingredient",
        "amount",
    )
    empty_value_display = "-empty-"
    list_display_links = ("recipe", "ingredient")
    save_on_top = True


admin.site.site_header = "Foodgram Administration"
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(AmountIngredient, AmountIngredientAdmin)
admin.site.unregister(Group)
