# Generated by Django 4.2.13 on 2024-05-16 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0003_rename_subscription_feedpublication_feedsubscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='email_frequency',
        ),
    ]
