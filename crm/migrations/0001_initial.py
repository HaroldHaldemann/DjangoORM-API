# Generated by Django 4.0.2 on 2023-06-09 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('company_name', models.CharField(blank=True, max_length=250, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False, verbose_name='Converted')),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Signed')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('amount', models.FloatField()),
                ('payment_due', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('event_status', models.BooleanField(default=False, verbose_name='Completed')),
                ('attendees', models.PositiveIntegerField()),
                ('event_date', models.DateTimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('contract', models.OneToOneField(limit_choices_to={'status': True}, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='crm.contract')),
            ],
        ),
    ]
