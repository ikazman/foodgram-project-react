# Generated by Django 3.0.5 on 2021-12-10 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20211209_1505'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipe',
            name='unique_recipe_pair',
        ),
    ]
