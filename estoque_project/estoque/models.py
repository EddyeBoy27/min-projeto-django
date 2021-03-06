from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Apedido(models.Model):
    apediid = models.AutoField(primary_key=True)
    acliid = models.ForeignKey(User, models.DO_NOTHING, db_column='acliid_id')
    apedidata = models.DateField(auto_now_add=True)
    apedistatus = models.SmallIntegerField(default=1)
    apedivenc = models.DateField(default=datetime.now() + timedelta(days=5))

    class Meta:
        managed = True
        db_table = 'apedido'


class Aproduto(models.Model):
    aprodid = models.AutoField(primary_key=True)
    aprodnome = models.CharField(max_length=255, verbose_name='Nome')
    aprodvalor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    aprodqntd = models.IntegerField(verbose_name='Quantidade')
    aprodativo = models.SmallIntegerField(verbose_name='Ativo')

    def __str__(self):
        return self.aprodnome

    def get_absolute_url(self):
        return reverse("produto:detail", kwargs={"pk": self.aprodid})

    class Meta:
        managed = True
        db_table = 'aproduto'
        verbose_name = 'Produto'


class Aprodutoinstancia(models.Model):
    aprinid = models.AutoField(primary_key=True)
    aprinid_acli = models.ForeignKey(User, models.DO_NOTHING, db_column="aprinid_acli")
    aprinid_apedi = models.ForeignKey(Apedido, models.DO_NOTHING, db_column="aprinid_apedi")
    aprinid_aprodid = models.ForeignKey(Aproduto, models.DO_NOTHING, db_column="aprinid_aprodid")
    aprinval = models.DecimalField(max_digits=10, decimal_places=2)
    aprinqnt = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'aprodutoinstancia'