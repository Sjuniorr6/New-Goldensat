from django.urls import path
from .views import (
    CadastroTipoProdutoView, EntradaProdutoView, EntradaProdutoModalView, UpdateCadastroTipoProdutoView, 
    UpdateEntradaProdutoView, DeleteCadastroTipoProdutoView, DeleteEntradaProdutoView,
    ListCadastroTipoProdutoView, ListEntradaProdutoView, DetailCadastroTipoProdutoView, 
    DetailEntradaProdutoView, CadastroProdutoModalView, BuscarEquipamentoView,
    EstoqueView, EstoqueAPIView, MovimentacoesAPIView
)

app_name = 'produtos'
urlpatterns = [
    # Listagem
    path('', ListCadastroTipoProdutoView.as_view(), name='listagem_produtos'),
    path('listagem/', ListCadastroTipoProdutoView.as_view(), name='list_cadastro_tipo_produto'),
    path('entradas/', ListEntradaProdutoView.as_view(), name='list_entrada_produto'),
    
    # Cadastro
    path('cadastro-tipo-produto/', CadastroTipoProdutoView.as_view(), name='cadastro_tipo_produto'),
    path('cadastro-produto-modal/', CadastroProdutoModalView.as_view(), name='cadastro_produto_modal'),
    path('entrada-produto/', EntradaProdutoView.as_view(), name='entrada_produto'),
    path('entrada-produto-modal/', EntradaProdutoModalView.as_view(), name='entrada_produto_modal'),
    
    # Edição
    path('update-cadastro-tipo-produto/<int:pk>/', UpdateCadastroTipoProdutoView.as_view(), name='update_cadastro_tipo_produto'),
    path('update-entrada-produto/<int:pk>/', UpdateEntradaProdutoView.as_view(), name='update_entrada_produto'),
    
    # Exclusão
    path('delete-cadastro-tipo-produto/<int:pk>/', DeleteCadastroTipoProdutoView.as_view(), name='delete_cadastro_tipo_produto'),
    path('delete-entrada-produto/<int:pk>/', DeleteEntradaProdutoView.as_view(), name='delete_entrada_produto'),
    
    # Detalhes
    path('detail-cadastro-tipo-produto/<int:pk>/', DetailCadastroTipoProdutoView.as_view(), name='detail_cadastro_tipo_produto'),
    path('detail-entrada-produto/<int:pk>/', DetailEntradaProdutoView.as_view(), name='detail_entrada_produto'),
    
    # Busca
    path('buscar-equipamento/', BuscarEquipamentoView.as_view(), name='buscar_equipamento'),
    
    # Estoque
    path('estoque/', EstoqueView.as_view(), name='estoque'),
    path('api/estoque/<int:produto_id>/', EstoqueAPIView.as_view(), name='estoque_api'),
    path('api/movimentacoes/<int:produto_id>/', MovimentacoesAPIView.as_view(), name='movimentacoes_api'),
]