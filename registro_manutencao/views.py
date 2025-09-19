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
from django.contrib import messages
from django.urls import reverse_lazy
import json
import traceback

from .models import registrodemanutencao, ImagemRegistro, retorno
from .forms import RegistroManutencaoForm, ImagemRegistroForm, RetornoForm, FiltroManutencaoForm


class ManutencaoListView(LoginRequiredMixin, ListView):
    """View para listar todos os registros de manutenção"""
    model = registrodemanutencao
    template_name = 'registro_manutencao/lista_manutencoes.html'
    context_object_name = 'manutencoes'
    paginate_by = 12

    def get_queryset(self):
        """Filtrar registros baseado nos filtros aplicados"""
        queryset = registrodemanutencao.objects.all()
        
        # Aplicar filtros se fornecidos
        form = FiltroManutencaoForm(self.request.GET)
        if form.is_valid():
            # Buscar por ID
            if form.cleaned_data.get('buscar_id'):
                queryset = queryset.filter(id__icontains=form.cleaned_data['buscar_id'])
            
            # Buscar por Nome
            if form.cleaned_data.get('buscar_nome'):
                queryset = queryset.filter(nome__nome_fantasia__icontains=form.cleaned_data['buscar_nome'])
            
            # Buscar por Equipamento
            if form.cleaned_data.get('buscar_equipamento'):
                queryset = queryset.filter(
                    Q(id_equipamentos__icontains=form.cleaned_data['buscar_equipamento']) |
                    Q(numero_equipamento__icontains=form.cleaned_data['buscar_equipamento'])
                )
            
            # Filtrar por Status
            if form.cleaned_data.get('status'):
                queryset = queryset.filter(status=form.cleaned_data['status'])
        
        return queryset.order_by('-data_criacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Registros de Manutenção'
        context['active_tab'] = 'manutencao'
        context['filter_form'] = FiltroManutencaoForm(self.request.GET)
        
        # Estatísticas
        total_manutencoes = registrodemanutencao.objects.count()
        pendentes = registrodemanutencao.objects.filter(status='Pendente').count()
        aprovadas = registrodemanutencao.objects.filter(status='Aprovado').count()
        expedidas = registrodemanutencao.objects.filter(status='expedido').count()
        
        context['stats'] = {
            'total': total_manutencoes,
            'pendentes': pendentes,
            'aprovadas': aprovadas,
            'expedidas': expedidas,
        }
        
        return context


class ManutencaoCreateView(LoginRequiredMixin, CreateView):
    """View para criar novo registro de manutenção"""
    model = registrodemanutencao
    form_class = RegistroManutencaoForm
    template_name = 'registro_manutencao/criar_manutencao.html'
    success_url = reverse_lazy('registro_manutencao:lista_manutencoes')

    def form_valid(self, form):
        messages.success(self.request, 'Registro de manutenção criado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar registro de manutenção. Verifique os dados.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Nova Manutenção'
        context['active_tab'] = 'manutencao'
        return context


class ManutencaoUpdateView(LoginRequiredMixin, UpdateView):
    """View para editar registro de manutenção"""
    model = registrodemanutencao
    form_class = RegistroManutencaoForm
    template_name = 'registro_manutencao/editar_manutencao.html'
    success_url = reverse_lazy('registro_manutencao:lista_manutencoes')

    def form_valid(self, form):
        messages.success(self.request, 'Registro de manutenção atualizado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar registro de manutenção. Verifique os dados.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Editar Manutenção #{self.object.id}'
        context['active_tab'] = 'manutencao'
        return context


class ManutencaoDetailView(LoginRequiredMixin, DetailView):
    """View para visualizar detalhes do registro de manutenção"""
    model = registrodemanutencao
    template_name = 'registro_manutencao/detalhes_manutencao.html'
    context_object_name = 'manutencao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Detalhes da Manutenção #{self.object.id}'
        context['active_tab'] = 'manutencao'
        
        # Buscar imagens relacionadas
        context['imagens'] = ImagemRegistro.objects.filter(registro=self.object)
        
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ManutencaoDeleteView(LoginRequiredMixin, View):
    """View para excluir registro de manutenção via AJAX"""
    
    def post(self, request, pk):
        try:
            manutencao = get_object_or_404(registrodemanutencao, pk=pk)
            manutencao_id = manutencao.id
            manutencao.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Registro de manutenção #{manutencao_id} excluído com sucesso!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao excluir registro: {str(e)}'
            })


@method_decorator(csrf_exempt, name='dispatch')
class ManutencaoStatusUpdateView(LoginRequiredMixin, View):
    """View para atualizar status do registro de manutenção via AJAX"""
    
    def post(self, request, pk):
        try:
            manutencao = get_object_or_404(registrodemanutencao, pk=pk)
            new_status = request.POST.get('status')
            
            if new_status in [choice[0] for choice in registrodemanutencao.STATUS_CHOICES]:
                manutencao.status = new_status
                manutencao.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Status atualizado para: {new_status}',
                    'new_status': new_status
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Status inválido'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao atualizar status: {str(e)}'
            })


class ImagemRegistroCreateView(LoginRequiredMixin, CreateView):
    """View para adicionar imagem ao registro"""
    model = ImagemRegistro
    form_class = ImagemRegistroForm
    template_name = 'registro_manutencao/adicionar_imagem.html'

    def form_valid(self, form):
        messages.success(self.request, 'Imagem adicionada com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('registro_manutencao:detalhes_manutencao', kwargs={'pk': self.object.registro.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Adicionar Imagem'
        context['active_tab'] = 'manutencao'
        return context


class RetornoListView(LoginRequiredMixin, ListView):
    """View para listar retornos"""
    model = retorno
    template_name = 'registro_manutencao/lista_retornos.html'
    context_object_name = 'retornos'
    paginate_by = 12

    def get_queryset(self):
        return retorno.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Retornos'
        context['active_tab'] = 'manutencao'
        return context


class RetornoCreateView(LoginRequiredMixin, CreateView):
    """View para criar novo retorno"""
    model = retorno
    form_class = RetornoForm
    template_name = 'registro_manutencao/criar_retorno.html'
    success_url = reverse_lazy('registro_manutencao:lista_retornos')

    def form_valid(self, form):
        messages.success(self.request, 'Retorno criado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Novo Retorno'
        context['active_tab'] = 'manutencao'
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ManutencaoBuscaView(LoginRequiredMixin, View):
    """View para busca de manutenções via AJAX"""
    
    def get(self, request):
        try:
            query = request.GET.get('q', '').strip()
            
            if len(query) < 2:
                return JsonResponse({
                    'success': False,
                    'message': 'Digite pelo menos 2 caracteres para buscar'
                })
            
            manutencoes = registrodemanutencao.objects.filter(
                Q(id__icontains=query) |
                Q(nome__nome_fantasia__icontains=query) |
                Q(tipo_produto__nome_produto__icontains=query) |
                Q(id_equipamentos__icontains=query)
            )[:10]  # Limitar a 10 resultados
            
            resultados = []
            for manutencao in manutencoes:
                resultados.append({
                    'id': manutencao.id,
                    'nome': f"Manutenção #{manutencao.id}",
                    'cliente': manutencao.nome.nome_fantasia if manutencao.nome else 'N/A',
                    'produto': manutencao.tipo_produto.nome_produto if manutencao.tipo_produto else 'N/A',
                    'status': manutencao.status,
                    'url': f'/manutencao/detalhes/{manutencao.id}/'
                })
            
            return JsonResponse({
                'success': True,
                'resultados': resultados
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro na busca: {str(e)}'
            })


@login_required
def dashboard_manutencao(request):
    """Dashboard com estatísticas de manutenção"""
    context = {
        'page_title': 'Dashboard de Manutenção',
        'active_tab': 'manutencao',
    }
    
    # Estatísticas gerais
    total_manutencoes = registrodemanutencao.objects.count()
    pendentes = registrodemanutencao.objects.filter(status='Pendente').count()
    aprovadas = registrodemanutencao.objects.filter(status='Aprovado').count()
    expedidas = registrodemanutencao.objects.filter(status='expedido').count()
    
    # Manutenções recentes
    manutencoes_recentes = registrodemanutencao.objects.all()[:5]
    
    # Estatísticas por tratativa
    tratativas_stats = {}
    for choice in registrodemanutencao.TRATATIVAS:
        count = registrodemanutencao.objects.filter(tratativa=choice[0]).count()
        if count > 0:
            tratativas_stats[choice[1]] = count
    
    context.update({
        'stats': {
            'total': total_manutencoes,
            'pendentes': pendentes,
            'aprovadas': aprovadas,
            'expedidas': expedidas,
        },
        'manutencoes_recentes': manutencoes_recentes,
        'tratativas_stats': tratativas_stats,
    })
    
    return render(request, 'registro_manutencao/dashboard.html', context)
