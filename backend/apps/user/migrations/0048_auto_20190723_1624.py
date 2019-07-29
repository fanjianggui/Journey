# Generated by Django 2.0.4 on 2019-07-23 08:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0047_auto_20190723_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='jwt_secret',
            field=models.UUIDField(default=uuid.UUID('f316f49f-a9e4-4b8a-89f1-4ca757cdc837'), verbose_name='用户jwt加密秘钥'),
        ),
    ]