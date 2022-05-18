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
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': '&nbsp;'}))

    class Meta:
        model = User
        fields = ('username', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = '&nbsp;'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = '&nbsp;'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = '&nbsp;'


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
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UpdateProfileForm(forms.ModelForm):
    current_year = datetime.now().year
    YEAR_CHOICES = list(map(int, range(1950, datetime.now().year + 1)))
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))

    class Meta:
        model = Profile
        fields = ('birthday',)


@login_required
def profile(request):
    template_name = 'users/profile.html'
    user = request.user
    form = UpdateUserForm(request.POST or None, instance=user)
    try:
        prof = request.user.profile
    except User.profile.RelatedObjectDoesNotExist:
        prof = None
    form_profile = UpdateProfileForm(
        request.POST or None, instance=prof)
    if request.method == 'POST':
        if form.is_valid() and form_profile.is_valid():
            form.save()
            try:
                form_profile.save()
            except IntegrityError:
                pass
            return redirect(reverse('profile'))
    context = {
        'form': form,
        'form_profile': form_profile,
        'user': user,
    }
    return render(request, template_name, context)


class MyLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = '&nbsp;'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = '&nbsp;'


"""def login(request):
    template = 'login.html'
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            print(1)
            cd = form.cleaned_data
            print(cd)
            user = authenticate(
                username=cd['username'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    context = {'form': form, }
    return render(request, template, context)"""
