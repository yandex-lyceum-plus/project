from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True, verbose_name='День рождения')

    class Meta:
        verbose_name = 'Дополнительное поле'
        verbose_name_plural = 'Дополнительные поля'
