# Generated by Django 4.1.7 on 2023-03-09 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='IsAvailable',
            field=models.BooleanField(default=True, help_text='もしfalseなら選択/表示ができない'),
        ),
        migrations.AlterField(
            model_name='room',
            name='IsAvailable',
            field=models.BooleanField(default=True, help_text='もしfalseなら選択/表示ができない'),
        ),
        migrations.AlterField(
            model_name='room',
            name='area',
            field=models.ForeignKey(limit_choices_to={'IsAvailable': True}, on_delete=django.db.models.deletion.PROTECT, to='Mainapp.area'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='place',
            field=models.ForeignKey(limit_choices_to={'IsAvailable': True}, on_delete=django.db.models.deletion.PROTECT, to='Mainapp.room'),
        ),
    ]