# Generated by Django 5.0.4 on 2024-04-11 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0004_alter_order_comments_alter_supplies_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]