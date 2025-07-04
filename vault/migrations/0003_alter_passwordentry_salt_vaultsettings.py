# Generated by Django 5.2.3 on 2025-06-17 11:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0002_passwordentry_salt'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordentry',
            name='salt',
            field=models.CharField(default=123, max_length=24),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='VaultSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salt', models.CharField(max_length=24)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
