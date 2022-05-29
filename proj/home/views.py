from django.shortcuts import render
from article.models import MainArticle, Category, Article, Rating
from django.db.models import Prefetch


def check_article(sp):
    while len(sp) < 3:
        sp.append(None)
    return(sp)


def homepage(request):
    template = 'home/homepage.html'
    categories = Category.objects.all()
    articles = MainArticle.objects.filter(is_published=True).order_by('?')
    sl = {}
    for i in articles:
        if i.category_id in sl:
            sl[i.category_id] += [i]
        else:
            sl[i.category_id] = [i]
    categories = sorted([{'category': Category.objects.filter(id=i).first(), 'articles': check_article(sl[i][:3])}
                         for i in sl], key=lambda x: x['category'].name)
    last_articles = Article.objects.filter(
        is_published=True).order_by('-published_date')[:4]
    ratings = Rating.objects.values('star', 'main_article',)
    sl = {}
    for i in ratings:
        if i['main_article'] in sl:
            sl[i['main_article']] += [int(i['star'])]
        else:
            sl[i['main_article']] = [int(i['star'])]
    most_popular_articles = sorted([{'main_aticle': MainArticle.objects.filter(
        id=i).first(), 'star': sum(sl[i])/len(sl[i]), 'category': Category.objects.filter(id=MainArticle.objects.filter(
            id=i).first().category_id).first()} for i in sl], key=lambda x: -x['star'])[:4]
    return render(request, template, {'categories': categories, 'last_articles': last_articles, 'most_popular_articles': most_popular_articles})
