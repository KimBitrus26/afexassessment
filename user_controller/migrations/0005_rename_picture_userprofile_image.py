# Generated by Django 4.0.6 on 2022-07-24 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_controller', '0004_alter_userprofile_bio_alter_userprofile_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='picture',
            new_name='image',
        ),
    ]