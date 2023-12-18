from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Length

from recipes.constants import MAX_HEX, MAX_LEN_TITLE, MAX_AMOUNT, MIN_AMOUNT
from users.models import User

models.CharField.register_lookup(Length)


class Tag(models.Model):
    """Tag model."""
    
    name = models.CharField(
        verbose_name='Tag name',
        max_length=MAX_LEN_TITLE,
        unique=True,
        help_text='Enter tag name'
    )
    slug = models.SlugField(
        verbose_name='Tag slug',
        max_length=MAX_LEN_TITLE,
        unique=True,
        help_text='Enter tag slug'
    )
    color = ColorField(
        verbose_name='HEX-code for color',
        max_length=MAX_HEX,
        unique=True,
        help_text='Choose color for tag'
    )


    class Meta:
        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient model."""
    
    name = models.CharField(
        verbose_name='Ingredient name',
        max_length=MAX_LEN_TITLE,
        help_text='Enter ingredient name'
    )
    measurement_unit = models.CharField(
        verbose_name='Measurement unit',
        max_length=MAX_LEN_TITLE,
        help_text='Enter measurement unit'
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_unit'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Recipe model."""
    
    name = models.CharField(
        verbose_name='Recipe name',
        max_length=MAX_LEN_TITLE,
        help_text='Enter recipe name'
    )
    text = models.TextField(
        verbose_name='Recipe text',
        help_text='Enter recipe text'
    )
    image = models.ImageField(
        verbose_name='Recipe image',
        upload_to='recipes/images/',
        help_text='Upload recipe image'
    )
    pub_date = models.DateTimeField(
        verbose_name='Publication date',
        auto_now_add=True,
        editable=False,
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Recipe author',
        help_text='Choose recipe author'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
        validators=[
            MinValueValidator(limit_value=MIN_AMOUNT,
                              message=f'At least {MIN_AMOUNT} minute!'),
            MaxValueValidator(limit_value=MAX_AMOUNT,
                              message=f'No more than {MAX_AMOUNT} minutes!'),
        ],
        help_text='Enter cooking time in minutes'
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='Tags',
        related_name='recipes',
        blank=True,
        help_text='Choose tags for recipe'
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        verbose_name='Ingredients',
        related_name='recipes',
        through='AmountIngredient',
        help_text='Choose ingredients and amount'
    )

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ('-pub_date',)
        constraints = (
            models.CheckConstraint(
                check=models.Q(name__length__gt=0),
                name='\n%(app_label)s_%(class)s_name is empty\n',
            ),
        )

    def __str__(self) -> str:
        return f'{self.name}. Автор: {self.author.username}'


class AmountIngredient(models.Model):
    """Ingredient amount model."""
    recipe = models.ForeignKey(
        to=Recipe,
        related_name='recipe_ingredient',
        on_delete=models.CASCADE,
        verbose_name='Recipe',
        help_text='Choose recipe for ingredient'
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ingredient',
        help_text='Choose ingredient for recipe'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Amount of ingredient',
        help_text='Enter amount of ingredient',
        validators=(
            MinValueValidator(
                limit_value=MIN_AMOUNT,
                message=f'At least {MIN_AMOUNT}!'),
            MaxValueValidator(
                limit_value=MAX_AMOUNT,
                message=f'No more than {MAX_AMOUNT}!')),
    )

    class Meta:
        verbose_name = 'Ingredient from recipe'
        verbose_name_plural = 'Ingredients from recipe'
        ordering = ('recipe',)

    def __str__(self):
        return (
            f'{self.ingredient.name} ({self.ingredient.measurement_unit}) - '
            f'{self.amount} '
        )


class UserRecipeRelation(models.Model):
    """Model for user-recipe relations."""
    user = models.ForeignKey(
        to=User,
        verbose_name='User',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
    )
    recipe = models.ForeignKey(
        to=Recipe,
        verbose_name='Recipe',
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related',
    )

    class Meta:
        abstract = True
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name=('\n%(app_label)s_%(class)s recipe already'
                      ' linked to this user\n'),
            ),
        )


class Favorite(UserRecipeRelation):
    """Model for favorite recipes."""
    date_added = models.DateTimeField(
        verbose_name='Date of addition',
        auto_now_add=True,
        editable=False,
    )

    class Meta(UserRecipeRelation.Meta):
        verbose_name = 'Favorite recipe'
        verbose_name_plural = 'Favorite recipes'

    def __str__(self):
        return f'{self.user} added {self.recipe} to Favorites'


class ShoppingCart(UserRecipeRelation):
    """Model for shopping cart."""
    class Meta(UserRecipeRelation.Meta):
        verbose_name = 'Recipe in shopping cart'
        verbose_name_plural = 'Recipes in shopping cart'

    def __str__(self):
        return f'{self.recipe} is in {self.user} shopping cart'
