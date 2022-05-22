# Generated by Django 3.2.13 on 2022-05-22 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20220522_1236'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='rating',
            name='rating_unique',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='article',
        ),
        migrations.AddField(
            model_name='rating',
            name='main_article',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='article.mainarticle', verbose_name='Статья'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='review',
            field=models.TextField(default=0, max_length=250, verbose_name='Отзыв'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(fields=('main_article', 'user'), name='rating_unique'),
        ),
    ]
