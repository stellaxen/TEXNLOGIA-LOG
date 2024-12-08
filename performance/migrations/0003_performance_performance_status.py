# Generated by Django 5.1.3 on 2024-11-30 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0002_performance_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='performance_status',
            field=models.CharField(choices=[('created', 'CREATED'), ('submitted', 'SUBMITTED'), ('reviewed', 'REVIEWED'), ('rejected', 'REJECTED'), ('approved', 'APPROVED'), ('scheduled', 'SCHEDULED')], default='created', max_length=20),
        ),
    ]
