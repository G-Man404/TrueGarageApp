# Generated by Django 5.0.4 on 2024-04-18 23:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0016_alter_task_engineer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='engineer',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Engineer', to='admin_app.engineer'),
        ),
    ]