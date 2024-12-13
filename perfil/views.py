import copy
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect

from perfil import models
from perfil import forms


class BasePerfil(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('cart', {}))
        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = models.PerfilUsuario.objects.filter(usuario=self.request.user).first()
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfilform':forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                ),
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'perfilform':forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                ),
            }

        self.userform = self.context['userform']
        self.perfilform = self.context['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(self.request, self.template_name, self.context)
    
    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                'Dados inválidos, por favor verifique as informações enviadas'
            )
            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            usuario = get_object_or_404(User, username=self.request.user.username)
            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            if not self.perfil:
                self.perfil.cleaned_data['usuario'] = usuario
                perfil = models.PerfilUsuario(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password,
            )

            if autentica:
                login(self.request, user=usuario)

        self.request.session['cart'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Cadastro realizado com sucesso!'
        )

        return redirect('perfil:criar')


class Update(BasePerfil):
    pass


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request, 
                'Usuário ou senha inválidos'    
            )
            return redirect('perfil:criar')
        
        usuario = authenticate(
            self.request,
            username=username,
            password=password    
        )

        if not usuario:
            messages.error(
                self.request, 
                'Usuário ou senha inválidos'    
            )
            return redirect('perfil:criar')
            
        login(self.request, user=usuario)
        messages.success(
            self.request, 
            'Login efetuado com sucesso'    
        )
        return redirect('produto:carrinho')


class Logout(View):
   def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('produto:lista')
