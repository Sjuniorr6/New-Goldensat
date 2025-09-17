from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Usuários
    path('', views.listar_usuarios, name='listar_usuarios'),
    path('criar/', views.criar_usuario, name='criar_usuario'),
    path('editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('detalhes/<int:user_id>/', views.detalhes_usuario, name='detalhes_usuario'),
    path('excluir/<int:user_id>/', views.excluir_usuario, name='excluir_usuario'),
    path('ativar/<int:user_id>/', views.ativar_usuario, name='ativar_usuario'),
    
    # Perfil do usuário
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
    
    # Setores
    path('setores/', views.listar_setores, name='listar_setores'),
    path('setores/criar/', views.criar_setor, name='criar_setor'),
    path('setores/editar/<int:setor_id>/', views.editar_setor, name='editar_setor'),
    
    # Permissões
    path('permissoes/', views.listar_permissoes, name='listar_permissoes'),
    path('permissoes/criar/', views.criar_permissao, name='criar_permissao'),
]
