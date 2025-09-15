from django.urls import path
from .views import (
    TicketListView, 
    TicketCreateView, 
    TicketDetailView, 
    TicketUpdateView, 
    TicketDeleteView,
    dashboard_tickets,
    TicketStatsAPIView
)

app_name = 'tickets'
urlpatterns = [
    path('', TicketListView.as_view(), name='lista_tickets'),
    path('dashboard/', dashboard_tickets, name='dashboard_tickets'),
    path('criar/', TicketCreateView.as_view(), name='criar_ticket'),
    path('detalhes/<int:pk>/', TicketDetailView.as_view(), name='detalhes_ticket'),
    path('editar/<int:pk>/', TicketUpdateView.as_view(), name='editar_ticket'),
    path('excluir/<int:pk>/', TicketDeleteView.as_view(), name='excluir_ticket'),
    path('api/stats/', TicketStatsAPIView.as_view(), name='ticket_stats_api'),
]
