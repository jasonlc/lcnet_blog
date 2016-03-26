from sets import Set

from django.db.models import Count
from .models import Category, Article


def category(request):
    category = Category.objects.filter(article__status=0).values('name').annotate(
            num_article=Count('article'))
    return {'categories': category,}

