from django.db import models
from django.conf import settings
from django.utils.text import slugify

import os
from PIL import Image

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produtos/%Y/%m')
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(default=0)
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(default='V', max_length=1, choices=(
        ('V', 'Variável'), ('S', 'Simples')  
    ))

    def __str__(self):
        return self.nome
    
    @staticmethod
    def redimencionar_imagem(img, new_width):
        caminho_img = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(caminho_img)
        original_width, original_height = img_pil.size

        if original_width <=  new_width:
            img_pil.close()
            return
        
        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            caminho_img,
            optimize=True,
            quality=50    
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_width = 800
        self.redimencionar_imagem(self.imagem, max_width)

    def get_preco_formatado(self):
        return f'R${self.preco_marketing:.2f}'
    get_preco_formatado.short_description = 'Preço'
    
    def get_preco_promocao_formatado(self):
        return f'R${self.preco_marketing_promocional:.2f}'
    get_preco_promocao_formatado.short_description = 'Preço Promoção'

class Variacao(models.Model):
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome