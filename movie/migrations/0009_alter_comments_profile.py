# Generated by Django 3.2.7 on 2021-09-19 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_comments_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.profile'),
        ),
    ]
