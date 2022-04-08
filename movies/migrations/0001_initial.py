# Generated by Django 3.2.11 on 2022-04-08 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('popularity', models.FloatField()),
                ('release_date', models.DateField()),
                ('genre', models.TextField()),
                ('score', models.FloatField()),
                ('poster_url', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
    ]
