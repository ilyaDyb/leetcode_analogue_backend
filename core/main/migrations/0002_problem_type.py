# Generated by Django 5.0.6 on 2024-06-30 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='type',
            field=models.CharField(choices=[('Algorithm', 'Algorithm'), ('SQL', 'SQL')], default='Algorithm', max_length=20),
        ),
    ]