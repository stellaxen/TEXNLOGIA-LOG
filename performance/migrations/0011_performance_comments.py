# Generated by Django 5.1.4 on 2025-01-03 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0010_alter_performance_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='comments',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
