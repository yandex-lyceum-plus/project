from django.shortcuts import render, redirect


def redirect_to_homepage(request):
    return redirect('homepage')


def categories(request):
    template_name = 'article/categories.html'
    extra = {}
    return render(request, template_name, extra)


def popular(request):
    template_name = 'article/popular.html'
    extra = {}
    return render(request, template_name, extra)


def new(request):
    template_name = 'article/new.html'
    extra = {}
    return render(request, template_name, extra)
