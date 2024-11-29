from django.contrib import admin
from pedido import models

class ItemPedidoInline(admin.TabularInline):
    model = models.ItemPedido
    extra = 1


@admin.register(models.Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInline,    
    ]


@admin.register(models.ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    ...
