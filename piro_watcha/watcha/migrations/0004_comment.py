# Generated by Django 2.0.7 on 2018-08-09 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcha', '0003_movie_poster'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200, verbose_name='댓글')),
            ],
        ),
    ]
