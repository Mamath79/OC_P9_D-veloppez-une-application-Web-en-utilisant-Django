# Generated by Django 5.1.1 on 2024-10-26 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_rename_body_review_commentaire_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
