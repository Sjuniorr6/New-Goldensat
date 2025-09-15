from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.ListClientesView.as_view(), name='listagem_clientes'),
    path('cadastrar/', views.ClienteModalView.as_view(), name='cadastrar_cliente'),
    path('detail/<int:pk>/', views.DetailClienteView.as_view(), name='detail_cliente'),
    path('update/<int:pk>/', views.UpdateClienteView.as_view(), name='update_cliente'),
    path('delete/<int:pk>/', views.DeleteClienteView.as_view(), name='delete_cliente'),
    path('api/clientes/', views.ApiClientesView.as_view(), name='api_clientes'),
]
