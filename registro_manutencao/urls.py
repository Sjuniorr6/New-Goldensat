from django.urls import path
from . import views

app_name = 'registro_manutencao'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_manutencao, name='dashboard'),
    
    # Listagem e CRUD de Manutenções
    path('', views.ManutencaoListView.as_view(), name='lista_manutencoes'),
    path('criar/', views.ManutencaoCreateView.as_view(), name='criar_manutencao'),
    path('editar/<int:pk>/', views.ManutencaoUpdateView.as_view(), name='editar_manutencao'),
    path('detalhes/<int:pk>/', views.ManutencaoDetailView.as_view(), name='detalhes_manutencao'),
    path('excluir/<int:pk>/', views.ManutencaoDeleteView.as_view(), name='excluir_manutencao'),
    path('status/<int:pk>/', views.ManutencaoStatusUpdateView.as_view(), name='atualizar_status'),
    
    # Imagens
    path('imagem/adicionar/', views.ImagemRegistroCreateView.as_view(), name='adicionar_imagem'),
    
    # Retornos
    path('retornos/', views.RetornoListView.as_view(), name='lista_retornos'),
    path('retornos/criar/', views.RetornoCreateView.as_view(), name='criar_retorno'),
    
    # Busca
    path('busca/', views.ManutencaoBuscaView.as_view(), name='busca_manutencoes'),
]