from django.views import View
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from produto.models import Variacao
from pedido.models import Pedido, ItemPedido
from utils import utils


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(*args, **kwargs)

    # FILTRA OS PEDIDOS A PARTIR DO USUARIO RELACIONADO
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs


class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class Fechar(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login'
            )
            return redirect('perfil:criar')
        
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Carrinho está vazio'
            )
            return redirect('produto:lista')
        
        carrinho = self.request.session['cart']
        carrinho_variacoes = [v for v in carrinho]
        db_variacoes = list(Variacao.objects.select_related('produto').filter(id__in=carrinho_variacoes))
        
        for variacao in db_variacoes:
            error_msg_estoque = ''
            vid = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['amount']
            preco_unt = carrinho[vid]['unit_price']
            preco_unt_promo = carrinho[vid]['unit_promotional_price']

            if qtd_carrinho > estoque:
                carrinho[vid]['amount'] = estoque
                carrinho[vid]['quantitative_price'] = estoque * preco_unt
                carrinho[vid]['quantitative_promotional_price'] = estoque * preco_unt_promo

                error_msg_estoque = 'Estoque insulficiente para alguns produtos, '\
                'reduzimos para a quantidade máxima em estoque'
                 
            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )
                self.request.session.save()
                return redirect('produto:carrinho')

        valor_total_carrinho = utils.cart_totals(carrinho)
        qtd_total_carrinho = utils.cart_total_qtd(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C'    
        )

        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['product_name'],
                    produtoId=v['product_id'],
                    variacao=v['variation_name'],
                    variacaoId=v['variation_id'],
                    preco=v['quantitative_price'],
                    preco_promocional=v['quantitative_promotional_price'],
                    quantidade=v['amount'],
                    imagem=v['image'],
                ) for v in carrinho.values()
            ]
        )

        del self.request.session['cart']
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }    
            )    
        )


class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    context_object_name = 'pedido'
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'


class Lista(DispatchLoginRequiredMixin ,ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = ['-id']
