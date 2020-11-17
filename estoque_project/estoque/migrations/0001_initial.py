# Generated by Django 3.1.3 on 2020-11-05 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aprodnome', models.CharField(help_text='Nome do produto', max_length=255)),
                ('aprodvalor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('aprodqntd', models.IntegerField(default=0.0)),
                ('aprodativo', models.SmallIntegerField(default=0)),
            ],
        ),
    ]
