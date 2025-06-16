from django.db.models import Sum
from datetime import date
from django.http import HttpResponse

from recipes.models import IngredientRecipe


def download_shopping_cart(request, author):
    ingredients = (
        IngredientRecipe.objects.filter(recipe__shopping_cart__author=author)
        .values('ingredient__name', 'ingredient__measurement_unit')
        .annotate(amount_sum=Sum('amount'))
        .order_by('ingredient__name')
    )
    today_str = date.today().strftime('%d-%m-%Y')
    lines = [f'Список покупок на: {today_str}\n']
    for item in ingredients:
        lines.append(f"{item['ingredient__name']} - {item['amount_sum']} {item['ingredient__measurement_unit']}")
    lines.append('\nFoodgram (2022)')
    content = '\n'.join(lines)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=shopping_list.txt'
    return response
