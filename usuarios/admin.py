from django.contrib import admin
from .models import Setor, PerfilUsuario, PermissaoSetor

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['get_nome_display', 'descricao', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'nome']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'setor', 'cargo', 'telefone', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'setor', 'data_criacao']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'cargo']
    ordering = ['user__first_name', 'user__last_name']
    raw_id_fields = ['user']

@admin.register(PermissaoSetor)
class PermissaoSetorAdmin(admin.ModelAdmin):
    list_display = ['setor', 'nome_permissao', 'descricao', 'ativo']
    list_filter = ['ativo', 'setor']
    search_fields = ['nome_permissao', 'descricao', 'setor__nome']
    ordering = ['setor', 'nome_permissao']
