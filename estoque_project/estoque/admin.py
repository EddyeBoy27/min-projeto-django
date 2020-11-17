from django.contrib import admin

from .models import Aproduto

@admin.register(Aproduto)


class AprodutoAdmin(admin.ModelAdmin):
    list_display = ('aprodnome', 'aprodvalor', 'aprodqntd', 'aprodativo')
# Register your models here.
