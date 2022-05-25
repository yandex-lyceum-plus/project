from django.shortcuts import get_object_or_404, render, redirect
from article.models import Category, MainArticle, Rating, Article
from home.views import chek_article


def redirect_to_homepage(request):
    return redirect('homepage')


def categories(request):
    template_name = 'article/categories.html'
    categories = Category.objects.all()
    articles = MainArticle.objects.filter(is_published=True).order_by('?')
    sl = {}
    for i in articles:
        if i.category_id in sl:
            sl[i.category_id] += [i]
        else:
            sl[i.category_id] = [i]
    categories = sorted([{'category': Category.objects.filter(id=i).first(), 'articles': chek_article(sl[i][:3])}
                   for i in sl], key=lambda x: x['category'].name)
    extra = {'categories': categories}
    return render(request, template_name, extra)


def popular(request):
    template_name = 'article/popular.html'
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
    extra = {'most_popular_articles': most_popular_articles}
    return render(request, template_name, extra)


def new(request):
    #! есче не новый артикл, а список новых
    template_name = 'article/new.html'
    last_articles = Article.objects.filter(is_published=True).order_by('-published_date')[:10]
    extra = {'last_articles': last_articles}
    return render(request, template_name, extra)


def read(request, pk):
    template_name = 'article/a/article.html'
    article = get_object_or_404(MainArticle.objects.filter(is_published=True), pk=pk)
    print(article.title)
    extra = {'article': article}
    return render(request, template_name, extra)
