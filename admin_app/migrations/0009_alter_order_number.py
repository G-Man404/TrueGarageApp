# Generated by Django 5.0.3 on 2024-03-28 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0008_alter_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
