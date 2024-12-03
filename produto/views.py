from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from produto import models

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    # paginate_by = 12


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Adicionar Produto')


class RemoverProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover Produto')


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')


class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')