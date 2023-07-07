# Generated by Django 3.2.20 on 2023-07-06 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_remove_uploadedfiles_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfiles',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
