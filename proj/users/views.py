from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.db.utils import IntegrityError
from django.urls import reverse
from users.models import Profile
from datetime import datetime
from django.urls import reverse
from article.models import Article


NBSP = ' '


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': NBSP}))

    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = NBSP
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = NBSP
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = NBSP


def signup(request):
    template_name = 'users/register.html'
    form = CreateUserForm(request.POST or None)
    form_error = ''
    if request.method == 'POST':
        if form.is_valid():
            if not User.objects.filter(email=form.cleaned_data['email']):
                form.save()
                return redirect(reverse('profile'))
            else:
                form_error = f'Почта {form.cleaned_data["email"]} уже используется'
    context = {'form': form, 'form_error': form_error}
    return render(request, template_name, context)


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
                                 attrs={'placeholder': 'Иван', 'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(
                                attrs={'placeholder': 'Иванов', 'class': 'form-control'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(
                            attrs={'placeholder': 'name@example.com', 'class': 'form-control'}))


class MyLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = NBSP
        self.fields['password'].widget.attrs['placeholder'] = NBSP


@login_required
def profile(request):
    template_name = 'users/profile/profile.html'
    user = request.user
    form = UpdateUserForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
    context = {
        'form': form,
        'user': user,
    }
    return render(request, template_name, context)


@login_required
def delete_profile(request):
    template_name = 'users/profile/delete.html'
    if request.method == 'POST':
        try:
            User.objects.filter(username=request.user).update(is_active=False)
            return redirect('homepage')
        except Exception as e:
            return render(request, template_name, {'e': e})
    return render(request, template_name)


@login_required
def contribution(request):
    template_name = 'users/profile/contribution.html'
    extra_context = {
        'articles': Article.objects.filter(author=request.user).order_by('published_date')
    }
    return render(request, template_name, extra_context)
