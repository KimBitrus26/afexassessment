# Generated by Django 4.0.6 on 2022-07-26 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_controller', '0008_userprofile_is_online_alter_friendrequest_accepted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='friend',
            new_name='friends',
        ),
        migrations.RemoveField(
            model_name='friends',
            name='is_friend',
        ),
    ]
