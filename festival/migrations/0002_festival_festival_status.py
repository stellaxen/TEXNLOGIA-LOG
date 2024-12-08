# Generated by Django 5.1.3 on 2024-11-30 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('festival', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='festival',
            name='festival_status',
            field=models.CharField(choices=[('created', 'CREATED'), ('submission', 'SUBMISSION'), ('assignment', 'ASSIGNMENT'), ('review', 'REVIEW'), ('scheduling', 'SCHEDULING'), ('final_submission', 'FINAL_SUBMISSION')], default='created', max_length=20),
        ),
    ]
