from django.db import models
from django.conf import settings

import os
from PIL import Image

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produtos/%Y/%m')
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField(default=0)
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(default='V', max_length=1, choices=(
        ('V', 'Variação'), ('S', 'Simples')  
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
        super().save(*args, **kwargs)

        max_width = 800
        self.redimencionar_imagem(self.imagem, max_width)


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