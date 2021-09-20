# Generated by Django 3.2.7 on 2021-09-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_alter_profile_motto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='motto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile/pic'),
        ),
    ]
