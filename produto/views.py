from django.views import View
from django.shortcuts import render, redirect, get_object_or_404, reverse
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
        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()

        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            # TODO: adicionar mensagens de conclusao e erro
            return redirect(http_referer)

        variation = get_object_or_404(models.Variacao, id=variation_id)
        product = variation.produto

        product_id = product.id
        product_name = product.nome
        variation_name = variation.nome or ''
        unit_price = variation.preco
        unit_promotional_price = variation.preco_promocional
        slug = product.slug
        image = product.imagem.name


        if variation.estoque < 1:
            # TODO: mensagem de erro de estoque 
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            amount_cart = cart[variation_id]['amount']
            amount_cart += 1

            if variation.estoque < amount_cart:
                # TODO: mensagem de erro de quantidade
                amount_cart = variation.estoque
                return redirect(http_referer)

            cart[variation_id]['amount'] = amount_cart
            cart[variation_id]['quantitative_price'] = unit_price * amount_cart
            cart[variation_id]['quantitative_promotional_price'] = unit_promotional_price * amount_cart
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'unit_promotional_price': unit_promotional_price,
                'quantitative_price': unit_price,
                'quantitative_promotional_price': unit_promotional_price,
                'amount': 1,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        # TODO: mensagem de sucesso
        return redirect(http_referer)


class RemoverProduto(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover Produto')


class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')


class Carrinho(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'produto/carrinho.html')