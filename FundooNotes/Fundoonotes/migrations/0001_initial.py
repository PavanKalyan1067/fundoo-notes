# Generated by Django 4.0.5 on 2022-08-02 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('reminder', models.TimeField(blank=True, null=True)),
                ('isArchive', models.BooleanField(default=False)),
                ('isTrash', models.BooleanField(default=False)),
                ('isPinned', models.BooleanField(default=False)),
            ],
        ),
    ]
