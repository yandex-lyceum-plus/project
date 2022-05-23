from re import M
from django.shortcuts import render
from article.models import MainArticle, Category, Article, Rating
from django.db.models import Prefetch


def homepage(request):
    template = 'home/homepage.html'
    categories = Category.objects.prefetch_related(Prefetch(
        'articles', queryset=MainArticle.objects.order_by('?'))).order_by('name')
    last_articles = Article.objects.filter(is_published=True).order_by('published_date')[:4]
    ratings = Rating.objects.values('star', 'main_article',)
    sl = {}
    for i in ratings:
        if i['main_article'] in sl:
            sl[i['main_article']] += [int(i['star'])]
        else:
            sl[i['main_article']] = [int(i['star'])]
    most_popular_articles = sorted([{'main_aticle': MainArticle.objects.filter(
        id=i).first(), 'star': sum(sl[i])/len(sl[i])} for i in sl], key=lambda x: -x['star'])[:4]
    return render(request, template, {'categories': categories, 'last_articles': last_articles, 'most_popular_articles': most_popular_articles})
