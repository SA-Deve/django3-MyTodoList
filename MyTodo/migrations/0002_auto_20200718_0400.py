# Generated by Django 3.0.7 on 2020-07-18 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyTodo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todomodel',
            name='dateCompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
