# Generated by Django 4.2.5 on 2023-10-09 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_apis', '0002_remove_influencer_package_recommendations'),
    ]

    operations = [
        migrations.AddField(
            model_name='influencer',
            name='description',
            field=models.TextField(default='abc'),
            preserve_default=False,
        ),
    ]
