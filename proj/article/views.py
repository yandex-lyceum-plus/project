from django.shortcuts import get_object_or_404, render, redirect
from article.models import Category, MainArticle, Rating, Article
from home.views import check_article
from django.urls import reverse


def redirect_to_homepage(request):
    return redirect('homepage')


def categories(request):
    template_name = 'article/categories.html'
    articles = MainArticle.objects.filter(is_published=True).order_by('?')
    category_dict = {}
    for i in articles:
        if i.category_id in category_dict:
            category_dict[i.category_id] += [i]
        else:
            category_dict[i.category_id] = [i]
    categories = sorted([{'category': Category.objects.get(id=i), 'articles': check_article(category_dict[i][:3])}
                         for i in category_dict], key=lambda x: x['category'].name)
    extra = {'categories': categories}
    return render(request, template_name, extra)


def popular(request):
    template_name = 'article/popular.html'
    ratings = Rating.objects.values('star', 'main_article',)
    article_dict = {}
    for i in ratings:
        if i['main_article'] in article_dict:
            article_dict[i['main_article']] += [int(i['star'])]
        else:
            article_dict[i['main_article']] = [int(i['star'])]
    most_popular_articles = sorted([{'main_aticle': MainArticle.objects.filter(is_published=True).get(id=i),
                                     'star': sum(article_dict[i])/len(article_dict[i]),
                                     'category': Category.objects.filter(id=MainArticle.objects.filter(is_published=True).get(id=i).category_id).first()}\
                                        for i in article_dict], key=lambda x: -x['star'])
    extra = {'most_popular_articles': most_popular_articles}
    return render(request, template_name, extra)


def new(request):
    template_name = 'article/new.html'
    last_articles = Article.objects.filter(is_published=True).order_by('-published_date')
    extra = {'last_articles': last_articles}
    return render(request, template_name, extra)


def read(request, pk):
    template_name = 'article/a/article.html'
    article = get_object_or_404(
        MainArticle.objects.filter(is_published=True), pk=pk)
    extra = {'article': article}
    return render(request, template_name, extra)


def read_article(request, pk):
    template_name = 'article/a/article.html'
    article = get_object_or_404(MainArticle.objects.filter(is_published=True), pk=pk)
    user_rate = None
    if request.user.is_authenticated:
        user_rate = Rating.objects.filter(main_article=article, user=request.user).first()
        if request.method == 'POST':
            new_rate = request.POST['rate']
            if new_rate.isdigit():
                if 0 <= int(new_rate) <= 10:
                    if user_rate:
                        user_rate.star = int(new_rate)
                        user_rate.save(update_fields=['star'])
                    else:
                        Rating.objects.create(star=new_rate, main_article=article, user=request.user)
                    return redirect(reverse('read', args=[article.id]))
    extra = {
        'article': article,
        'user_rate': user_rate,
        'category': Category.objects.filter(id=article.category_id).first(),
        'second_aritcles': [i for i in article.articles.all()]
    }
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
    if search_querry:
        articles = [{'main_aticle': i, 'category': Category.objects.filter(id=i.category_id).first(
        )} for i in MainArticle.objects.filter(is_published=True, title__icontains=search_querry)]
    else:
        articles = None
    extra = {'articles': articles}
    return render(request, template_name, extra)


def read_second_article(request, pk):
    template_name = 'article/a/second_article.html'
    article = get_object_or_404(Article.objects.all(), pk=pk)
    extra = {'article': article}
    return render(request, template_name, extra)
