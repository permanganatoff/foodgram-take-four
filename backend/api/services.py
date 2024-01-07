from io import StringIO

from django.db.models import Sum

from recipes.models import AmountIngredient


def generate_shopping_cart_text(request):
    text_stream = StringIO()
    text_stream.write('Список покупок\n')
    text_stream.write('Ингредиент - Единица измерения - Количество\n')
    shopping_cart = (
        AmountIngredient.objects.select_related('recipe', 'ingredient')
        .filter(recipe__recipes_shoppingcart_related__user=request.user)
        .values_list(
            'ingredient__name',
            'ingredient__measurement_unit')
        .annotate(amount=Sum('amount'))
        .order_by('ingredient__name')
    )
    lines = (' - '.join(str(field) for field in item) + '\n'
             for item in shopping_cart)
    text_stream.writelines(lines)
    return text_stream.getvalue()
