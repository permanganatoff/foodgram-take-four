from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from recipes.constants import ADMIN_INLINE_EXTRA
from recipes.models import (
    AmountIngredient,
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag,
)


class IngredientInline(admin.TabularInline):
    model = AmountIngredient
    extra = ADMIN_INLINE_EXTRA


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'pub_date',
        'display_ingredients',
        'display_image',
        'display_favorites_count',
    )
    fields = (
        ('name', 'tags',),
        ('text', 'cooking_time'),
        ('author', 'image'),
    )
    search_fields = (
        'name',
        'author__username',
        'tags__name',
    )
    list_filter = ('name', 'author__username', 'tags__name')
    list_display_links = ('name', 'author')
    raw_id_fields = ('author',)
    inlines = (IngredientInline,)

    @admin.display(description='Ingredients')
    def display_ingredients(self, obj):
        ingredients_list = [
            ingredient.name for ingredient in obj.ingredients.all()]
        if ingredients_list:
            return ', '.join(ingredients_list)
        return '-'

    @admin.display(description='Photo')
    def display_image(self, obj):
        return mark_safe(
            f"<img src={obj.image.url} width='70' height='35' border='3'>")

    @admin.display(description='In favorites')
    def display_favorites_count(self, obj):
        return obj.recipes_favorite_related.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color')
    list_display_links = ('name', 'color')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
    list_display_links = ('user', 'recipe')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'date_added')
    search_fields = ('user__username', 'recipe__name')
    list_display_links = ('user', 'recipe')


@admin.register(AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


admin.site.site_header = 'Foodgram Administration'
admin.site.unregister(Group)
