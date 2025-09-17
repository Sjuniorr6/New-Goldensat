from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import Requisicoes
from .forms import RequisicaoForm
from produtos.models import EntradaProduto, CadastroTipoProduto
from produtos.logger_config import produtos_logger
import traceback

class ListRequisicoesView(ListView):
    model = Requisicoes
    template_name = 'requisicoes/listagem_requisicoes.html'
    context_object_name = 'requisicoes'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        try:
            produtos_logger.info(f"GET /requisicoes/ - Usuário: {request.user}")
            produtos_logger.info(f"GET - Parâmetros: {request.GET}")
            produtos_logger.info(f"GET - Headers: {dict(request.headers)}")
            
            # Verificar se é uma requisição AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                produtos_logger.info("Requisição AJAX detectada - renderizando cards parciais")
                queryset = self.get_queryset()
                produtos_logger.info(f"GET - Queryset retornado: {queryset.count()} itens")
                return render(request, 'requisicoes/cards_requisicoes.html', {
                    'requisicoes': queryset
                })
            
            return super().get(request, *args, **kwargs)
            
        except Exception as e:
            produtos_logger.error(f"Erro em ListRequisicoesView: {str(e)}")
            produtos_logger.error(traceback.format_exc())
            return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Filtrar apenas requisições pendentes na listagem
        queryset = Requisicoes.objects.select_related('nome', 'tipo_produto').filter(status='Pendente').order_by('-data')
        
        # Filtros
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        cliente = self.request.GET.get('cliente', '')
        
        produtos_logger.info(f"Filtros recebidos - Search: '{search}', Status: '{status}', Cliente: '{cliente}'")
        produtos_logger.info(f"Requisições pendentes encontradas: {queryset.count()}")
        
        if search:
            produtos_logger.info(f"Aplicando filtro de busca: '{search}'")
            # Tentar buscar por ID primeiro (se for número)
            try:
                search_id = int(search)
                queryset = queryset.filter(id=search_id)
                produtos_logger.info(f"Busca por ID {search_id}: {queryset.count()} resultados")
            except ValueError:
                # Se não for número, buscar por nome
                queryset = queryset.filter(nome__nome__icontains=search)
                produtos_logger.info(f"Busca por nome '{search}': {queryset.count()} resultados")
        
        if status:
            queryset = queryset.filter(status=status)
            
        if cliente:
            queryset = queryset.filter(nome__id=cliente)
        
        produtos_logger.info(f"Resultado final: {queryset.count()} requisições")
        return queryset

@method_decorator(csrf_exempt, name='dispatch')
class RequisicaoModalView(CreateView):
    model = Requisicoes
    form_class = RequisicaoForm
    template_name = 'requisicoes/modal_requisicao.html'

    def get(self, request, *args, **kwargs):
        try:
            produtos_logger.info(f"GET /requisicoes/cadastrar/ - Carregando modal")
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        except Exception as e:
            produtos_logger.error(f"Erro ao carregar modal: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'Erro ao carregar formulário'
            })

    def post(self, request, *args, **kwargs):
        try:
            produtos_logger.info(f"POST /requisicoes/cadastrar/ - Usuário: {request.user}")
            
            form = self.form_class(request.POST)
            
            if form.is_valid():
                requisicao = form.save()
                produtos_logger.info(f"Requisição {requisicao.id} criada com sucesso")
                
                return JsonResponse({
                    'success': True,
                    'message': f'Requisição {requisicao.id} criada com sucesso!',
                    'requisicao_id': requisicao.id
                })
            else:
                produtos_logger.warning(f"Erro de validação no formulário: {form.errors}")
                return JsonResponse({
                    'success': False,
                    'message': 'Erro de validação',
                    'errors': form.errors
                })
                
        except Exception as e:
            produtos_logger.error(f"Erro em RequisicaoModalView: {str(e)}")
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro interno do servidor'
            })

@method_decorator(csrf_exempt, name='dispatch')
class DetailRequisicaoView(DetailView):
    model = Requisicoes
    template_name = 'requisicoes/modal_detalhes_requisicao.html'

    def get(self, request, *args, **kwargs):
        try:
            requisicao = self.get_object()
            produtos_logger.info(f"GET /requisicoes/detail/{requisicao.id}/ - Usuário: {request.user}")
            
            return render(request, self.template_name, {
                'requisicao': requisicao
            })
            
        except Exception as e:
            produtos_logger.error(f"Erro em DetailRequisicaoView: {str(e)}")
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro ao carregar detalhes da requisição'
            })

@method_decorator(csrf_exempt, name='dispatch')
class UpdateRequisicaoView(View):
    def get(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            requisicao = get_object_or_404(Requisicoes, pk=pk)
            produtos_logger.info(f"GET /requisicoes/update/{requisicao.id}/ - Usuário: {request.user}")
            
            # Criar formulário simples
            form = RequisicaoForm(instance=requisicao)
            
            return render(request, 'requisicoes/modal_editar_requisicao.html', {
                'form': form,
                'requisicao': requisicao
            })
            
        except Exception as e:
            produtos_logger.error(f"Erro em UpdateRequisicaoView GET: {str(e)}")
            produtos_logger.error(traceback.format_exc())
            print(f"DEBUG: Erro capturado: {str(e)}")
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            
            # Retornar página de erro simples
            return render(request, 'requisicoes/modal_editar_requisicao.html', {
                'form': None,
                'requisicao': None,
                'error': str(e)
            })

    def post(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            requisicao = get_object_or_404(Requisicoes, pk=pk)
            produtos_logger.info(f"POST /requisicoes/update/{requisicao.id}/ - Usuário: {request.user}")
            
            form = RequisicaoForm(request.POST, instance=requisicao)
            
            if form.is_valid():
                requisicao = form.save()
                produtos_logger.info(f"Requisição {requisicao.id} atualizada com sucesso")
                
                return JsonResponse({
                    'success': True,
                    'message': f'Requisição {requisicao.id} atualizada com sucesso!'
                })
            else:
                produtos_logger.warning(f"Erro de validação na atualização: {form.errors}")
                return JsonResponse({
                    'success': False,
                    'message': 'Erro de validação',
                    'errors': form.errors
                })
                
        except Exception as e:
            produtos_logger.error(f"Erro em UpdateRequisicaoView POST: {str(e)}")
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro interno do servidor'
            })

@method_decorator(csrf_exempt, name='dispatch')
class DeleteRequisicaoView(DeleteView):
    model = Requisicoes

    def post(self, request, *args, **kwargs):
        try:
            requisicao = self.get_object()
            requisicao_id = requisicao.id
            produtos_logger.info(f"POST /requisicoes/delete/{requisicao_id}/ - Usuário: {request.user}")
            
            requisicao.delete()
            produtos_logger.info(f"Requisição {requisicao_id} excluída com sucesso")
            
            return JsonResponse({
                'success': True,
                'message': f'Requisição {requisicao_id} excluída com sucesso!'
            })
            
        except Exception as e:
            produtos_logger.error(f"Erro em DeleteRequisicaoView: {str(e)}")
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro ao excluir requisição'
            })

class VerificarEstoqueView(View):
    """View para verificar estoque disponível via AJAX"""
    
    def post(self, request):
        try:
            produto_id = request.POST.get('produto_id')
            quantidade = request.POST.get('quantidade')
            
            if not produto_id or not quantidade:
                return JsonResponse({
                    'success': False,
                    'message': 'Produto e quantidade são obrigatórios'
                })
            
            try:
                quantidade = int(quantidade)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Quantidade deve ser um número válido'
                })
            
            # Calcular estoque disponível
            entradas = EntradaProduto.objects.filter(codigo_produto_id=produto_id)
            estoque_total = sum(entrada.quantidade for entrada in entradas)
            
            if quantidade > estoque_total:
                return JsonResponse({
                    'success': False,
                    'message': f'Estoque insuficiente! Disponível: {estoque_total} unidades. Solicitado: {quantidade} unidades.',
                    'estoque_disponivel': estoque_total,
                    'quantidade_solicitada': quantidade
                })
            
            return JsonResponse({
                'success': True,
                'message': f'Estoque disponível: {estoque_total} unidades',
                'estoque_disponivel': estoque_total,
                'quantidade_solicitada': quantidade
            })
            
        except Exception as e:
            produtos_logger.error(f"Erro em VerificarEstoqueView: {str(e)}")
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro interno do servidor'
            })

class VerificarEstoqueRequisicaoView(View):
    """View para verificar estoque disponível para requisições via AJAX"""
    
    def post(self, request):
        try:
            produto_id = request.POST.get('produto_id')
            quantidade = request.POST.get('quantidade')
            
            if not produto_id or not quantidade:
                return JsonResponse({
                    'success': False,
                    'message': 'Produto e quantidade são obrigatórios'
                })
            
            try:
                quantidade = int(quantidade)
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Quantidade deve ser um número válido'
                })
            
            produto = get_object_or_404(CadastroTipoProduto, id=produto_id)
            estoque_disponivel = produto.get_estoque_disponivel()
            
            if quantidade <= estoque_disponivel:
                return JsonResponse({
                    'success': True,
                    'estoque_disponivel': estoque_disponivel,
                    'quantidade_solicitada': quantidade,
                    'message': f'Estoque disponível: {estoque_disponivel} unidades'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'estoque_disponivel': estoque_disponivel,
                    'quantidade_solicitada': quantidade,
                    'message': f'Estoque insuficiente! Disponível: {estoque_disponivel} unidades. Solicitado: {quantidade} unidades.'
                })
                
        except Exception as e:
            produtos_logger.error(f'Erro ao verificar estoque para requisição: {str(e)}')
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro interno do servidor'
            })

@method_decorator(csrf_exempt, name='dispatch')
class AprovarRequisicaoView(View):
    """View para aprovar uma requisição"""
    
    def post(self, request, pk):
        try:
            produtos_logger.info(f'POST /requisicoes/aprovar/{pk}/ - Usuário: {request.user}')
            produtos_logger.info(f'Dados recebidos: {dict(request.POST)}')
            produtos_logger.info(f'Headers: {dict(request.headers)}')
            
            requisicao = get_object_or_404(Requisicoes, id=pk)
            produtos_logger.info(f'Requisição encontrada: ID {requisicao.id}, Status: {requisicao.status}')
            
            # Verificar se a requisição pode ser aprovada
            if requisicao.status not in ['Pendente', 'Configurado']:
                produtos_logger.warning(f'Requisição {pk} não pode ser aprovada. Status atual: {requisicao.status}')
                return JsonResponse({
                    'success': False,
                    'message': f'Requisição não pode ser aprovada. Status atual: {requisicao.status}'
                })
            
            # Aprovar a requisição
            requisicao.status = 'Aprovado pelo CEO'
            requisicao.save()
            
            produtos_logger.info(f'Requisição {requisicao.id} aprovada pelo CEO com sucesso')
            
            return JsonResponse({
                'success': True,
                'message': 'Requisição aprovada com sucesso!',
                'new_status': requisicao.status
            })
            
        except Exception as e:
            produtos_logger.error(f'Erro ao aprovar requisição {pk}: {str(e)}')
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro interno do servidor'
            })

@method_decorator(csrf_exempt, name='dispatch')
class ReprovarRequisicaoView(View):
    """View para reprovar uma requisição"""
    
    def post(self, request, pk):
        try:
            requisicao = get_object_or_404(Requisicoes, id=pk)
            
            # Verificar se a requisição pode ser reprovada
            if requisicao.status not in ['Pendente', 'Configurado']:
                return JsonResponse({
                    'success': False,
                    'message': f'Requisição não pode ser reprovada. Status atual: {requisicao.status}'
                })
            
            # Reprovar a requisição
            requisicao.status = 'Reprovado pelo CEO'
            requisicao.save()
            
            produtos_logger.info(f'Requisição {requisicao.id} reprovada pelo CEO')
            
            return JsonResponse({
                'success': True,
                'message': 'Requisição reprovada com sucesso!',
                'new_status': requisicao.status
            })
            
        except Exception as e:
            produtos_logger.error(f'Erro ao reprovar requisição {pk}: {str(e)}')
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro interno do servidor'
            })

class HistoricoRequisicoesView(ListView):
    """View para exibir o histórico completo de requisições"""
    model = Requisicoes
    template_name = 'requisicoes/historico_requisicoes.html'
    context_object_name = 'requisicoes'
    paginate_by = 50

    def get_queryset(self):
        queryset = Requisicoes.objects.select_related('nome', 'tipo_produto').order_by('-data')
        
        # Filtros
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        cliente = self.request.GET.get('cliente', '')
        data_inicio = self.request.GET.get('data_inicio', '')
        data_fim = self.request.GET.get('data_fim', '')
        
        produtos_logger.info(f"Filtros do histórico - Search: '{search}', Status: '{status}', Cliente: '{cliente}', Data: '{data_inicio}' a '{data_fim}'")
        
        if search:
            # Tentar buscar por ID primeiro (se for número)
            try:
                search_id = int(search)
                queryset = queryset.filter(id=search_id)
            except ValueError:
                # Se não for número, buscar por nome do cliente
                queryset = queryset.filter(nome__nome__icontains=search)
        
        if status:
            queryset = queryset.filter(status=status)
            
        if cliente:
            queryset = queryset.filter(nome__id=cliente)
        
        if data_inicio:
            try:
                from datetime import datetime
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                queryset = queryset.filter(data__date__gte=data_inicio_obj)
            except ValueError:
                pass
        
        if data_fim:
            try:
                from datetime import datetime
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                queryset = queryset.filter(data__date__lte=data_fim_obj)
            except ValueError:
                pass
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar estatísticas
        total_requisicoes = Requisicoes.objects.count()
        aprovadas = Requisicoes.objects.filter(status='Aprovado pelo CEO').count()
        reprovadas = Requisicoes.objects.filter(status='Reprovado pelo CEO').count()
        pendentes = Requisicoes.objects.filter(status='Pendente').count()
        
        context.update({
            'total_requisicoes': total_requisicoes,
            'aprovadas': aprovadas,
            'reprovadas': reprovadas,
            'pendentes': pendentes,
            'filtros_ativos': any([
                self.request.GET.get('search'),
                self.request.GET.get('status'),
                self.request.GET.get('cliente'),
                self.request.GET.get('data_inicio'),
                self.request.GET.get('data_fim')
            ])
        })
        
        return context

class ConfiguracaoView(View):
    template_name = 'configuracao/configuracao.html'

    def get(self, request, *args, **kwargs):
        try:
            # Filtrar apenas requisições com status "Configurado" e "Aprovado pelo CEO"
            requisicoes = Requisicoes.objects.select_related('nome', 'tipo_produto').filter(
                status__in=['Configurado', 'Aprovado pelo CEO']
            ).order_by('-data')
            
            context = {
                'page_title': 'Configurações do Sistema',
                'active_tab': 'configuracao',
                'requisicoes': requisicoes
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(f"Erro na view de configurações: {e}")
            import traceback
            traceback.print_exc()
            # Retornar uma lista vazia em caso de erro
            context = {
                'page_title': 'Configurações do Sistema',
                'active_tab': 'configuracao',
                'requisicoes': []
            }
            return render(request, self.template_name, context)

@method_decorator(csrf_exempt, name='dispatch')
class AlterarStatusView(View):
    """View para alterar o status de uma requisição"""
    
    def post(self, request, pk):
        try:
            import json
            data = json.loads(request.body)
            novo_status = data.get('status')
            
            produtos_logger.info(f'POST /requisicoes/alterar-status/{pk}/ - Usuário: {request.user}')
            produtos_logger.info(f'Novo status: {novo_status}')
            
            requisicao = get_object_or_404(Requisicoes, id=pk)
            status_anterior = requisicao.status
            
            # Validar se o novo status é válido
            status_validos = ['Pendente', 'Configurado', 'Aprovado pelo CEO', 'Reprovado pelo CEO', 'Expedido']
            if novo_status not in status_validos:
                return JsonResponse({
                    'success': False,
                    'message': f'Status inválido: {novo_status}'
                })
            
            # Se o status for "Aprovado pelo CEO", mudar para "Expedido"
            if novo_status == 'Aprovado pelo CEO':
                novo_status = 'Expedido'
                produtos_logger.info(f'Status alterado de "Aprovado pelo CEO" para "Expedido"')
            
            # Armazenar status anterior para o signal
            requisicao._previous_status = status_anterior
            
            # Alterar o status
            requisicao.status = novo_status
            requisicao.save()
            
            produtos_logger.info(f'Status da requisição {pk} alterado de "{status_anterior}" para "{novo_status}"')
            
            return JsonResponse({
                'success': True,
                'message': f'Status alterado de "{status_anterior}" para "{novo_status}" com sucesso!',
                'novo_status': novo_status,
                'status_anterior': status_anterior
            })
            
        except Exception as e:
            produtos_logger.error(f'Erro ao alterar status da requisição {pk}: {str(e)}')
            produtos_logger.error(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': 'Erro interno do servidor'
            })

class HistoricoExpedicaoView(ListView):
    """View para exibir o histórico de requisições expedidas"""
    model = Requisicoes
    template_name = 'requisicoes/historico_expedicao.html'
    context_object_name = 'requisicoes'
    paginate_by = 20

    def get_queryset(self):
        # Filtrar apenas requisições com status "Expedido"
        queryset = Requisicoes.objects.select_related('nome', 'tipo_produto').filter(
            status='Expedido'
        ).order_by('-data')
        
        # Filtros
        search = self.request.GET.get('search', '')
        cliente = self.request.GET.get('cliente', '')
        data_inicio = self.request.GET.get('data_inicio', '')
        data_fim = self.request.GET.get('data_fim', '')
        
        produtos_logger.info(f"Filtros do histórico de expedição - Search: '{search}', Cliente: '{cliente}', Data: '{data_inicio}' a '{data_fim}'")
        
        if search:
            # Tentar buscar por ID primeiro (se for número)
            try:
                search_id = int(search)
                queryset = queryset.filter(id=search_id)
            except ValueError:
                # Se não for número, buscar por nome do cliente
                queryset = queryset.filter(nome__nome__icontains=search)
        
        if cliente:
            queryset = queryset.filter(nome__id=cliente)
        
        if data_inicio:
            try:
                from datetime import datetime
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                queryset = queryset.filter(data__date__gte=data_inicio_obj)
            except ValueError:
                pass
        
        if data_fim:
            try:
                from datetime import datetime
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                queryset = queryset.filter(data__date__lte=data_fim_obj)
            except ValueError:
                pass
        
        produtos_logger.info(f"Requisições expedidas encontradas: {queryset.count()}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar estatísticas
        total_expedidas = Requisicoes.objects.filter(status='Expedido').count()
        
        context.update({
            'page_title': 'Histórico de Expedição',
            'active_tab': 'historico_expedicao',
            'total_expedidas': total_expedidas,
            'filtros_ativos': any([
                self.request.GET.get('search'),
                self.request.GET.get('cliente'),
                self.request.GET.get('data_inicio'),
                self.request.GET.get('data_fim')
            ])
        })
        
        return context
