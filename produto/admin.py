from django.contrib import admin
from produto import models

class VariacaoInline(admin.TabularInline):
    model = models.Variacao
    extra = 1


@admin.register(models.Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao_curta', 'get_preco_formatado', 'get_preco_promocao_formatado']

    inlines = [
        VariacaoInline,    
    ]


@admin.register(models.Variacao)
class VariacaoAdmin(admin.ModelAdmin):
    ...
