# Generated by Django 4.0.6 on 2022-07-24 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_controller', '0006_remove_friendrequest_user_friendrequest_from_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_friend', to='user_controller.userprofile'),
        ),
        migrations.AlterField(
            model_name='friends',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_friend', to=settings.AUTH_USER_MODEL),
        ),
    ]