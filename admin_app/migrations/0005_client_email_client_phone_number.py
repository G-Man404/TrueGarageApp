# Generated by Django 5.0.3 on 2024-03-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_alter_engineer_user_alter_client_user_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AddField(
            model_name='client',
            name='phone_number',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
