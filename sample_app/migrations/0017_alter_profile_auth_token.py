# Generated by Django 4.1.3 on 2023-05-17 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample_app', '0016_alter_profile_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='auth_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
