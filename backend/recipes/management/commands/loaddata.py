import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient, Tag

logging.basicConfig(
    filename=f'{settings.BASE_DIR}/data/loaddata.log',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Upload data to Ingredients and Tags'

    def handle(self, *args, **kwargs):
        logger.info('Upload data to Ingredients and Tags is starting.')

        ingredients_file = open(
            f'{settings.BASE_DIR}/data/ingredients.json',
            encoding='utf-8')
        try:
            ingredients_data = json.load(ingredients_file)
            for item in ingredients_data:
                Ingredient.objects.get_or_create(**item)
        except FileNotFoundError as ingredients_error:
            logger.error(f'{ingredients_error}: Ingredients file not found')
            raise CommandError('Ingredients file not found')
        finally:
            ingredients_file.close()

        tags_file = open(
            f'{settings.BASE_DIR}/data/tags.json',
            encoding='utf-8')
        try:
            tags_data = json.load(tags_file)
            for item in tags_data:
                Tag.objects.get_or_create(**item)
        except FileNotFoundError as tags_error:
            logger.error(f'{tags_error}: Tags file not found')
            raise CommandError('Tags file not found')
        finally:
            tags_file.close()

        logger.info('Upload data to Ingredients and Tags is complete.')
