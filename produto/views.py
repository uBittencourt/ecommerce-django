from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View


class ListaProdutos(ListView):
    ...


class DetalheProduto(View):
    ...


class AdicionarProduto(View):
    ...


class RemoverProduto(View):
    ...


class Finalizar(View):
    ...


class Carrinho(View):
    ...