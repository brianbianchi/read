# Generated by Django 4.2.13 on 2024-06-05 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0004_remove_feed_email_frequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='num_pubs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='feed',
            name='num_subs',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='publication',
            name='num_feeds',
            field=models.IntegerField(default=0),
        ),
    ]
