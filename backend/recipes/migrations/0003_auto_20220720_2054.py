# Generated by Django 3.2.14 on 2022-07-20 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'verbose_name': 'Ингредиент к рецепту', 'verbose_name_plural': 'Ингредиенты к рецептам'},
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient'),
        ),
    ]
