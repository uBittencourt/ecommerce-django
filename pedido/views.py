from django.views import View
from django.shortcuts import render
from django.http import HttpResponse


class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagar Pedido')


class Fechar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Fechar Pedido')


class Detalhe(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe Pedido')
