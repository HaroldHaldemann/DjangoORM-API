# Generated by Django 4.0.2 on 2023-06-09 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='support_contact',
            field=models.ForeignKey(blank=True, limit_choices_to={'team': 'SUPPORT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(limit_choices_to={'status': True}, on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='crm.client'),
        ),
        migrations.AddField(
            model_name='contract',
            name='sales_contact',
            field=models.ForeignKey(blank=True, limit_choices_to={'team': 'SALES'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(blank=True, limit_choices_to={'team': 'SALES'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
