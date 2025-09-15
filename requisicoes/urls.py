from django.urls import path
from . import views

app_name = 'requisicoes'

urlpatterns = [
    path('', views.ListRequisicoesView.as_view(), name='listagem_requisicoes'),
    path('cadastrar/', views.RequisicaoModalView.as_view(), name='cadastrar_requisicao'),
    path('detail/<int:pk>/', views.DetailRequisicaoView.as_view(), name='detail_requisicao'),
    path('update/<int:pk>/', views.UpdateRequisicaoView.as_view(), name='update_requisicao'),
    path('delete/<int:pk>/', views.DeleteRequisicaoView.as_view(), name='delete_requisicao'),
    path('verificar-estoque/', views.VerificarEstoqueView.as_view(), name='verificar_estoque'),
    path('verificar-estoque-requisicao/', views.VerificarEstoqueRequisicaoView.as_view(), name='verificar_estoque_requisicao'),
    path('aprovar/<int:pk>/', views.AprovarRequisicaoView.as_view(), name='aprovar_requisicao'),
    path('reprovar/<int:pk>/', views.ReprovarRequisicaoView.as_view(), name='reprovar_requisicao'),
    path('historico/', views.HistoricoRequisicoesView.as_view(), name='historico_requisicoes'),
    path('configuracao/', views.ConfiguracaoView.as_view(), name='configuracao'),
    path('alterar-status/<int:pk>/', views.AlterarStatusView.as_view(), name='alterar_status'),
]
