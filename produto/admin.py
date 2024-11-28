from django.contrib import admin
from produto import models

class VariacaoInline(admin.TabularInline):
    model = models.Variacao


@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [
        VariacaoInline,    
    ]


@admin.register(models.Variacao)
class VariacaoAdmin(admin.ModelAdmin):
    ...
