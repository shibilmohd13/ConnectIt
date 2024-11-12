# Generated by Django 4.1.1 on 2022-10-29 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=30)),
                ('message', models.TextField(max_length=1000)),
                ('file', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Read', 'Read')], max_length=15)),
            ],
        ),
    ]
