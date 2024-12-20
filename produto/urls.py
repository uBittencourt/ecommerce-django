from django.urls import path
from produto import views


app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('adicionar/', views.AdicionarProduto.as_view(), name='adicionar'),
    path('remover/', views.RemoverProduto.as_view(), name='remover'),
    path('finalizar/', views.Finalizar.as_view(), name='finalizar'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('busca/', views.Busca.as_view(), name='busca'),
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe'),
]
