# Generated by Django 3.1.3 on 2020-11-18 19:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apedido',
            fields=[
                ('apediid', models.AutoField(primary_key=True, serialize=False)),
                ('apedidata', models.DateField(auto_now_add=True)),
                ('apedistatus', models.SmallIntegerField(default=1)),
                ('apedivenc', models.DateField(default=datetime.datetime(2020, 11, 23, 19, 3, 28, 25977))),
                ('acliid', models.ForeignKey(db_column='acliid_id', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'apedido',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Aproduto',
            fields=[
                ('aprodid', models.AutoField(primary_key=True, serialize=False)),
                ('aprodnome', models.CharField(max_length=255, verbose_name='Nome')),
                ('aprodvalor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor')),
                ('aprodqntd', models.IntegerField(verbose_name='Quantidade')),
                ('aprodativo', models.SmallIntegerField(verbose_name='Ativo')),
            ],
            options={
                'verbose_name': 'Produto',
                'db_table': 'aproduto',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Aprodutoinstancia',
            fields=[
                ('aprinid', models.AutoField(primary_key=True, serialize=False)),
                ('aprinval', models.DecimalField(decimal_places=2, max_digits=10)),
                ('aprinqnt', models.IntegerField()),
                ('aprinid_acli', models.ForeignKey(db_column='aprinid_acli', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('aprinid_apedi', models.ForeignKey(db_column='aprinid_apedi', on_delete=django.db.models.deletion.DO_NOTHING, to='estoque.apedido')),
                ('aprinid_aprodid', models.ForeignKey(db_column='aprinid_aprodid', on_delete=django.db.models.deletion.DO_NOTHING, to='estoque.aproduto')),
            ],
            options={
                'db_table': 'aprodutoinstancia',
                'managed': True,
            },
        ),
    ]
