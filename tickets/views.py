from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
import json
import traceback

from .models import TicketModel
from .forms import TicketForm, TicketUpdateForm

class TicketListView(LoginRequiredMixin, ListView):
    """View para listar todos os tickets"""
    model = TicketModel
    template_name = 'tickets/lista_tickets.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        """Filtrar tickets baseado no usuário e permissões"""
        queryset = TicketModel.objects.all()
        
        # Se não for staff, mostrar apenas seus próprios tickets
        if not self.request.user.is_staff:
            queryset = queryset.filter(usuario=self.request.user)
        
        # Filtros opcionais
        status = self.request.GET.get('status')
        setor = self.request.GET.get('setor')
        prioridade = self.request.GET.get('prioridade')
        
        if status:
            queryset = queryset.filter(status=status)
        if setor:
            queryset = queryset.filter(setor=setor)
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade)
        
        return queryset.order_by('-data_criacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sistema de Tickets'
        context['active_tab'] = 'tickets'
        context['status_choices'] = TicketModel.STATUS_CHOICES
        context['setor_choices'] = TicketModel.SETORES_CHOICES
        context['prioridade_choices'] = TicketModel.PRIORIDADE_CHOICES
        return context

@method_decorator(csrf_exempt, name='dispatch')
class TicketCreateView(LoginRequiredMixin, CreateView):
    """View para criar novo ticket via AJAX"""
    model = TicketModel
    form_class = TicketForm
    template_name = 'tickets/modal_criar_ticket.html'

    def get(self, request, *args, **kwargs):
        """Retorna o formulário para criação de ticket"""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Processa a criação do ticket"""
        try:
            form = self.form_class(request.POST, user=request.user)
            
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.usuario = request.user
                ticket.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Ticket #{ticket.id} criado com sucesso!',
                    'ticket_id': ticket.id
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro de validação',
                    'errors': form.errors
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

class TicketDetailView(LoginRequiredMixin, DetailView):
    """View para visualizar detalhes do ticket"""
    model = TicketModel
    template_name = 'tickets/modal_detalhes_ticket.html'
    context_object_name = 'ticket'

    def get_queryset(self):
        """Filtrar tickets baseado no usuário e permissões"""
        queryset = TicketModel.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(usuario=self.request.user)
        return queryset

@method_decorator(csrf_exempt, name='dispatch')
class TicketUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar ticket via AJAX"""
    model = TicketModel
    form_class = TicketUpdateForm
    template_name = 'tickets/modal_editar_ticket.html'

    def get(self, request, *args, **kwargs):
        """Retorna o formulário para edição do ticket"""
        ticket = get_object_or_404(TicketModel, pk=kwargs['pk'])
        
        # Verificar permissões
        if not request.user.is_staff and ticket.usuario != request.user:
            return JsonResponse({
                'success': False,
                'message': 'Você não tem permissão para editar este ticket'
            })
        
        form = self.form_class(instance=ticket)
        return render(request, self.template_name, {
            'form': form,
            'ticket': ticket
        })

    def post(self, request, *args, **kwargs):
        """Processa a atualização do ticket"""
        try:
            ticket = get_object_or_404(TicketModel, pk=kwargs['pk'])
            
            # Verificar permissões
            if not request.user.is_staff and ticket.usuario != request.user:
                return JsonResponse({
                    'success': False,
                    'message': 'Você não tem permissão para editar este ticket'
                })
            
            form = self.form_class(request.POST, instance=ticket)
            
            if form.is_valid():
                ticket = form.save()
                
                # Se status mudou para resolvido, atualizar data de resolução
                if ticket.status == 'Resolvido' and not ticket.data_resolucao:
                    from django.utils import timezone
                    ticket.data_resolucao = timezone.now()
                    ticket.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Ticket #{ticket.id} atualizado com sucesso!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro de validação',
                    'errors': form.errors
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

@method_decorator(csrf_exempt, name='dispatch')
class TicketDeleteView(LoginRequiredMixin, DetailView):
    """View para excluir ticket via AJAX"""
    model = TicketModel

    def post(self, request, *args, **kwargs):
        """Processa a exclusão do ticket"""
        try:
            ticket = get_object_or_404(TicketModel, pk=kwargs['pk'])
            
            # Verificar permissões
            if not request.user.is_staff and ticket.usuario != request.user:
                return JsonResponse({
                    'success': False,
                    'message': 'Você não tem permissão para excluir este ticket'
                })
            
            ticket_id = ticket.id
            ticket.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Ticket #{ticket_id} excluído com sucesso!'
            })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

def dashboard_tickets(request):
    """Dashboard com estatísticas dos tickets"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Estatísticas gerais
    total_tickets = TicketModel.objects.count()
    tickets_pendentes = TicketModel.objects.filter(status='Pendente').count()
    tickets_em_andamento = TicketModel.objects.filter(status='Em Andamento').count()
    tickets_resolvidos = TicketModel.objects.filter(status='Resolvido').count()
    
    # Se não for staff, filtrar apenas seus tickets
    if not request.user.is_staff:
        total_tickets = TicketModel.objects.filter(usuario=request.user).count()
        tickets_pendentes = TicketModel.objects.filter(usuario=request.user, status='Pendente').count()
        tickets_em_andamento = TicketModel.objects.filter(usuario=request.user, status='Em Andamento').count()
        tickets_resolvidos = TicketModel.objects.filter(usuario=request.user, status='Resolvido').count()
    
    # Tickets recentes
    tickets_recentes = TicketModel.objects.all()[:5]
    if not request.user.is_staff:
        tickets_recentes = TicketModel.objects.filter(usuario=request.user)[:5]
    
    context = {
        'page_title': 'Dashboard de Tickets',
        'active_tab': 'tickets',
        'total_tickets': total_tickets,
        'tickets_pendentes': tickets_pendentes,
        'tickets_em_andamento': tickets_em_andamento,
        'tickets_resolvidos': tickets_resolvidos,
        'tickets_recentes': tickets_recentes,
    }
    
    return render(request, 'tickets/dashboard_tickets.html', context)

@method_decorator(csrf_exempt, name='dispatch')
class TicketStatsAPIView(LoginRequiredMixin, View):
    """API para retornar estatísticas dos tickets"""
    
    def get(self, request):
        """Retorna estatísticas dos tickets em JSON"""
        try:
            # Estatísticas gerais
            total_tickets = TicketModel.objects.count()
            tickets_pendentes = TicketModel.objects.filter(status='Pendente').count()
            tickets_em_andamento = TicketModel.objects.filter(status='Em Andamento').count()
            tickets_resolvidos = TicketModel.objects.filter(status='Resolvido').count()
            
            # Se não for staff, filtrar apenas seus tickets
            if not request.user.is_staff:
                total_tickets = TicketModel.objects.filter(usuario=request.user).count()
                tickets_pendentes = TicketModel.objects.filter(usuario=request.user, status='Pendente').count()
                tickets_em_andamento = TicketModel.objects.filter(usuario=request.user, status='Em Andamento').count()
                tickets_resolvidos = TicketModel.objects.filter(usuario=request.user, status='Resolvido').count()
            
            return JsonResponse({
                'success': True,
                'stats': {
                    'total': total_tickets,
                    'pendentes': tickets_pendentes,
                    'em_andamento': tickets_em_andamento,
                    'resolvidos': tickets_resolvidos,
                    'total_pendentes': tickets_pendentes + tickets_em_andamento  # Total de tickets que precisam de atenção
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao buscar estatísticas: {str(e)}'
            })