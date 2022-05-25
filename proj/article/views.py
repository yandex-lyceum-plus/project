from django.shortcuts import get_object_or_404, render, redirect
from article.models import Category, MainArticle, Rating, Article
from home.views import chek_article
from django import forms
from article.validators import validate_rating


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
    last_articles = Article.objects.filter(
        is_published=True).order_by('-published_date')[:10]
    extra = {'last_articles': last_articles}
    return render(request, template_name, extra)


def read(request, pk):
    template_name = 'article/a/article.html'
    article = get_object_or_404(
        MainArticle.objects.filter(is_published=True), pk=pk)
    authenticated = False
    user_rate = None
    if request.user.is_authenticated:
        authenticated = True
        user_rate = Rating.objects.filter(
            main_article=article, user=request.user).first()
        if request.method == 'POST':
            new_rate = request.POST['rate']
            if new_rate.isdigit():
                if 0 <= int(new_rate) <= 10:
                    if user_rate:
                        user_rate.star = int(new_rate)
                        user_rate.save(update_fields=['star'])
                    else:
                        Rating.objects.create(
                            star=new_rate, main_article=article, user=request.user)
    extra = {'article': article, 'user_rate': user_rate,
             'authenticated': authenticated,
             'category': Category.objects.filter(id=article.category_id).first(),
             'second_aritcles': [i for i in article.articles.all()]}
    return render(request, template_name, extra)


def category(request, pk):
    template_name = 'article/category.html'
    category = get_object_or_404(Category.objects.all(), pk=pk)
    articles = MainArticle.objects.filter(
        category_id=category.id, is_published=True)
    extra = {'category': category, 'articles': articles}
    return render(request, template_name, extra)


def search_articles(request):
    template_name = 'article/search_templ.html'
    search_querry = request.GET.get('search', '')

    ratings = Rating.objects.values('star', 'main_article',)
    sl = {}
    for i in ratings:
        if i['main_article'] in sl:
            sl[i['main_article']] += [int(i['star'])]
        else:
            sl[i['main_article']] = [int(i['star'])]
    if search_querry:
        articles = sorted([{'main_aticle': MainArticle.objects.filter(
            id=i, title__icontains=search_querry).first(), 'star': sum(sl[i])/len(sl[i]), 'category': Category.objects.filter(id=MainArticle.objects.filter(
                id=i).first().category_id).first()} for i in sl], key=lambda x: -x['star'])[:4]
    else:
        articles = None
    extra = {'articles': articles}
    return render(request, template_name, extra)


def read_second_article(request, pk):
    template_name = 'article/a/second_article.html'
    article = get_object_or_404(Article.objects.all(), pk=pk)
    extra = {'article': article}
    return render(request, template_name, extra)
