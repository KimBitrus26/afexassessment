# Generated by Django 4.0.6 on 2022-07-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_controller', '0009_rename_friend_userprofile_friends_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]
