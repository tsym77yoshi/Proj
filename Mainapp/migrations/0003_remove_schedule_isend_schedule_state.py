# Generated by Django 4.1.7 on 2023-03-10 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0002_alter_area_isavailable_alter_room_isavailable_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='IsEnd',
        ),
        migrations.AddField(
            model_name='schedule',
            name='state',
            field=models.IntegerField(choices=[(1, '使用前'), (2, '使用中'), (3, '終了後')], default=1, help_text='部屋の使用を使用前/使用中/終了後'),
        ),
    ]
