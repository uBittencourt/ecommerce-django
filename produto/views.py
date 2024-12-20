from django.views import View
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.db.models import Q

from produto import models
from perfil.models import PerfilUsuario
from django.contrib.auth.models import User

class ListaProdutos(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6


class Busca(ListaProdutos):
    def get_queryset(self):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset()
        
        if not termo:
            return qs 
        
        self.request.session['termo'] = termo
    
        qs = qs.filter(nome__icontains=termo)
        self.request.session.save()
        return qs


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
            messages.error(
                self.request,
                'Produto não existe.'    
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variacao, id=variation_id)
        product = variation.produto

        product_id = product.id
        product_name = product.nome
        variation_name = variation.nome or ''
        unit_price = variation.preco
        unit_promotional_price = variation.preco_promocional
        amount = 1
        slug = product.slug
        image = product.imagem.name


        if variation.estoque < 1:
            messages.error(
                self.request,
                f'Estoque insulficiente'    
            ) 
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            amount_cart = cart[variation_id]['amount']
            amount_cart += 1

            if variation.estoque < amount_cart:
                messages.error(
                    self.request,
                    f'Estoque insulficiente para {amount_cart}x no '
                    f'produto "{product_name} {variation_name}". Adicionamos {variation.estoque}x '
                    'no seu carrinho.'    
                )
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

        try:
            messages.success(
                self.request, 
                f'Produto {product_name} {variation_name} adicionado ao seu '
                f'carrinho {amount_cart}x'
            )
        except:
            messages.success(
                self.request, 
                f'Produto {product_name} {variation_name} adicionado ao seu '
                f'carrinho {amount}x'
            )
        return redirect(http_referer)


class RemoverProduto(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER', reverse('produto:lista'))
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            return redirect(http_referer)
        
        if not self.request.session.get('cart'):
            return redirect(http_referer)
        
        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)
        
        cart = self.request.session['cart'][variation_id]

        messages.success(
            self.request,
            f'Produto {cart['product_name']} {cart['variation_name']} '
            f'removido do seu carrinho.'    
        )

        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(http_referer)


class Finalizar(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        
        perfil = PerfilUsuario.objects.filter(usuario=self.request.user).exists()
        data_perfil = get_object_or_404(PerfilUsuario, usuario=self.request.user)

        if not perfil:
            messages.error(
                self.request,
                'Usuário sem perfil.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Carrinho vazio.'
            )
            return redirect('produto:lista')

        print(self.request.session['cart'])
        context = {
            'usuario': data_perfil,
            'carrinho': self.request.session['cart']    
        }

        return render(
            self.request, 
            'produto/finalizar.html',
            context
        )


class Carrinho(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'produto/carrinho.html')