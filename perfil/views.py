from django.views import View
from django.shortcuts import render
from django.http import HttpResponse


class Criar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Criar Perfil')


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar Perfil')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
   def get(self, *args, **kwargs):
        return HttpResponse('Logout')
