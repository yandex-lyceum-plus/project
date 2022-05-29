from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.contrib.auth.decorators import login_required
from article.models import Article
from django.core.handlers.wsgi import WSGIRequest
from markitup.widgets import MarkItUpWidget
from article.models import Article


class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('text',)
    
    text = forms.CharField(label='Текст статьи', widget=MarkItUpWidget())


@login_required
def edit_article(request: WSGIRequest, pk):
    article = get_object_or_404(Article, id=pk)
    if article.author.id != request.user.id:
        return redirect('homepage')
    form = UpdateArticleForm(instance=article)
    extra = {
        'article': article,
        'form': form,
    }
    return render(request, 'edit/edit_article.html', extra)
