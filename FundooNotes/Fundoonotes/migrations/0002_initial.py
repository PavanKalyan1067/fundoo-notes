# Generated by Django 4.0.5 on 2022-08-02 18:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labels', '0001_initial'),
        ('Fundoonotes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='collaborator',
            field=models.ManyToManyField(blank=True, related_name='collaborator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notes',
            name='label',
            field=models.ManyToManyField(blank=True, to='labels.labels'),
        ),
        migrations.AddField(
            model_name='notes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]