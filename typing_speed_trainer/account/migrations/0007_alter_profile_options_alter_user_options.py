# Generated by Django 4.0.5 on 2022-10-31 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_profile_are_results_shown_profile_is_email_shown'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
