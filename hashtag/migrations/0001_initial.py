# Generated by Django 4.1.7 on 2023-03-15 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=20, unique=True)),
                ('ref_count', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'hashtag',
            },
        ),
    ]
