# Generated by Django 4.2.2 on 2023-09-22 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_app', '0011_alter_userlessoninfo_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlessoninfo',
            name='status',
            field=models.CharField(blank=True, max_length=12),
        ),
    ]
