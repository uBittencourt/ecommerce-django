from django.template import Library
from utils import utils

register = Library()


@register.filter
def formata_preco(valor):
    return utils.formata_preco(valor)


@register.filter
def cart_total_qtd(cart):
    return utils.cart_total_qtd(cart)


@register.filter
def cart_totals(cart):
    return utils.cart_totals(cart)
