from django.contrib import admin
from perfil import models

@admin.register(models.PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    ...
