# Generated by Django 4.2 on 2024-12-05 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumapp', '0003_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='topics',
            field=models.ManyToManyField(null=True, to='forumapp.topic'),
        ),
    ]
