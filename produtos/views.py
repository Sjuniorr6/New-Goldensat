from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db import models
import json
from .models import CadastroTipoProduto, EntradaProduto, MovimentacaoEstoque
from .forms import CadastroTipoProdutoForm, EntradaProdutoForm
from .logger_config import produtos_logger
# Create your views here.
class CadastroTipoProdutoView(CreateView):
    model = CadastroTipoProduto
    form_class = CadastroTipoProdutoForm
    template_name = 'produtos/cadastro_tipo_produto.html'
    success_url = reverse_lazy('cadastro_tipo_produto')
    
class EntradaProdutoView(ListView):
    model = EntradaProduto
    template_name = 'produtos/entrada_produto.html'
    context_object_name = 'object_list'
    paginate_by = 20
    
    def get(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info("GET - EntradaProdutoView (Lista) iniciado")
        produtos_logger.info(f"GET - Request path: {request.path}")
        produtos_logger.info(f"GET - User: {request.user}")
        
        try:
            response = super().get(request, *args, **kwargs)
            produtos_logger.info(f"GET - Lista carregada com {len(response.context_data['object_list'])} entradas")
            produtos_logger.info("=" * 50)
            return response
        except Exception as e:
            produtos_logger.error(f"GET - Erro ao carregar lista: {e}")
            produtos_logger.info("=" * 50)
            raise
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = CadastroTipoProduto.objects.all()
        produtos_logger.info(f"GET - Contexto preparado com {len(context['produtos'])} produtos")
        return context

@method_decorator(csrf_exempt, name='dispatch')
class EntradaProdutoModalView(CreateView):
    """View para entrada de produto via modal"""
    model = EntradaProduto
    form_class = EntradaProdutoForm
    
    def post(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info("POST - EntradaProdutoModalView iniciado")
        produtos_logger.info(f"POST - Dados recebidos: {len(request.POST)} campos")
        
        try:
            form = self.form_class(request.POST)
            produtos_logger.info(f"POST - Formulário validado: {form.is_valid()}")
            if not form.is_valid():
                produtos_logger.warning(f"POST - Formulário inválido: {form.errors}")
            
            if form.is_valid():
                codigo_produto = form.cleaned_data['codigo_produto']
                id_equipamento = form.cleaned_data['id_equipamento']
                data = form.cleaned_data['data']
                nova_quantidade = form.cleaned_data['quantidade']
                
                produtos_logger.info(f"POST - Produto: {codigo_produto.nome_produto}")
                produtos_logger.info(f"POST - ID equipamento: {id_equipamento}")
                produtos_logger.info(f"POST - Data: {data}")
                produtos_logger.info(f"POST - Nova quantidade: {nova_quantidade}")
                
                # Verificar se existe entrada com mesmo produto (independente de data e ID)
                entrada_existente = EntradaProduto.objects.filter(
                    codigo_produto=codigo_produto
                ).first()
                
                if entrada_existente:
                    produtos_logger.info(f"POST - Entrada existente encontrada: ID {entrada_existente.id}")
                    produtos_logger.info("POST - Atualizando entrada existente")
                    # Atualizar quantidade e adicionar ID do equipamento
                    quantidade_anterior = entrada_existente.quantidade
                    entrada_existente.quantidade += nova_quantidade
                    produtos_logger.info(f"POST - Quantidade: {quantidade_anterior} + {nova_quantidade} = {entrada_existente.quantidade}")
                    
                    # Adicionar o novo ID de equipamento à lista (se não existir)
                    produtos_logger.info(f"POST - Adicionando ID equipamento: {id_equipamento}")
                    entrada_existente.add_id_equipamento(id_equipamento)
                    produtos_logger.info(f"POST - Total de IDs após adição: {entrada_existente.get_quantidade_ids()}")
                    
                    # Atualizar outros campos se necessário
                    entrada_existente.valor_nota = form.cleaned_data['valor_nota']
                    entrada_existente.numero_nota_fiscal = form.cleaned_data['numero_nota_fiscal']
                    entrada_existente.save()
                    produtos_logger.info("POST - Entrada atualizada com sucesso")
                    
                    total_ids = entrada_existente.get_quantidade_ids()
                    
                    return JsonResponse({
                        'success': True,
                        'message': f'Quantidade atualizada! Produto: {codigo_produto.nome_produto} - Quantidade: {quantidade_anterior} + {nova_quantidade} = {entrada_existente.quantidade} (Total de IDs: {total_ids})',
                        'quantity_updated': True,
                        'entrada': {
                            'id': entrada_existente.id,
                            'produto': entrada_existente.codigo_produto.nome_produto,
                            'quantidade_anterior': quantidade_anterior,
                            'quantidade_adicionada': nova_quantidade,
                            'quantidade_total': entrada_existente.quantidade,
                            'total_ids_equipamentos': total_ids,
                            'data': entrada_existente.data.strftime('%d/%m/%Y %H:%M')
                        }
                    })
                else:
                    produtos_logger.info("POST - Criando nova entrada")
                    # Criar nova entrada
                    entrada = form.save()
                    produtos_logger.info(f"POST - Nova entrada criada: ID {entrada.id}")
                    # Inicializar o campo ids_equipamentos com o primeiro ID
                    entrada.ids_equipamentos = id_equipamento
                    entrada.save()
                    produtos_logger.info(f"POST - IDs equipamentos inicializados: {entrada.ids_equipamentos}")
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'Nova entrada registrada com sucesso!',
                        'entrada': {
                            'id': entrada.id,
                            'produto': entrada.codigo_produto.nome_produto,
                            'quantidade': entrada.quantidade,
                            'numero_nota_fiscal': entrada.numero_nota_fiscal
                        }
                    })
            else:
                produtos_logger.warning(f"POST - Formulário inválido: {form.errors}")
                return JsonResponse({
                    'success': False,
                    'message': 'Erro no formulário',
                    'errors': form.errors
                })
        except Exception as e:
            produtos_logger.error(f"POST - Erro na EntradaProdutoModalView: {e}")
            produtos_logger.error(f"POST - Tipo do erro: {type(e)}")
            import traceback
            produtos_logger.error(f"POST - Traceback: {traceback.format_exc()}")
            produtos_logger.info("=" * 50)
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

class UpdateCadastroTipoProdutoView(UpdateView):
    model = CadastroTipoProduto
    form_class = CadastroTipoProdutoForm
    template_name = 'produtos/cadastro_tipo_produto.html'
    success_url = reverse_lazy('cadastro_tipo_produto')
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            form = self.form_class(request.POST, instance=self.object)
            if form.is_valid():
                produto = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Produto atualizado com sucesso!',
                    'produto': {
                        'id': produto.id,
                        'nome_produto': produto.nome_produto,
                        'fabricante': produto.fabricante,
                        'valor_unitario': str(produto.valor_unitario) if produto.valor_unitario else '0.00'
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro no formulário',
                    'errors': form.errors
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

class UpdateEntradaProdutoView(UpdateView):
    model = EntradaProduto
    form_class = EntradaProdutoForm
    template_name = 'produtos/entrada_produto.html'
    success_url = reverse_lazy('entrada_produto')
    
    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            form = self.form_class(request.POST, instance=self.object)
            if form.is_valid():
                entrada = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Entrada atualizada com sucesso!',
                    'entrada': {
                        'id': entrada.id,
                        'produto': entrada.codigo_produto.nome_produto,
                        'quantidade': entrada.quantidade,
                        'numero_nota_fiscal': entrada.numero_nota_fiscal
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro no formulário',
                    'errors': form.errors
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

class EstoqueView(ListView):
    """View para exibir o estoque disponível de todos os produtos"""
    model = CadastroTipoProduto
    template_name = 'produtos/estoque.html'
    context_object_name = 'produtos'
    paginate_by = 20
    
    def get_queryset(self):
        """Retorna produtos com informações de estoque"""
        produtos = CadastroTipoProduto.objects.all()
        
        # Adicionar informações de estoque para cada produto
        for produto in produtos:
            produto.estoque_disponivel = produto.get_estoque_disponivel()
            produto.total_entradas = MovimentacaoEstoque.objects.filter(
                produto=produto, tipo='entrada'
            ).aggregate(total=models.Sum('quantidade'))['total'] or 0
            produto.total_saidas = MovimentacaoEstoque.objects.filter(
                produto=produto, tipo='saida'
            ).aggregate(total=models.Sum('quantidade'))['total'] or 0
        
        return produtos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Controle de Estoque'
        context['active_tab'] = 'estoque'
        return context

@method_decorator(csrf_exempt, name='dispatch')
class EstoqueAPIView(View):
    """API para consultar estoque de um produto específico"""
    
    def get(self, request, produto_id):
        try:
            produto = CadastroTipoProduto.objects.get(id=produto_id)
            estoque_disponivel = produto.get_estoque_disponivel()
            
            return JsonResponse({
                'success': True,
                'produto_id': produto.id,
                'produto_nome': produto.nome_produto,
                'estoque_disponivel': estoque_disponivel
            })
            
        except CadastroTipoProduto.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Produto não encontrado'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

@method_decorator(csrf_exempt, name='dispatch')
class MovimentacoesAPIView(View):
    """API para buscar movimentações de um produto específico"""
    
    def get(self, request, produto_id):
        try:
            produto = CadastroTipoProduto.objects.get(id=produto_id)
            movimentacoes = MovimentacaoEstoque.objects.filter(produto=produto).order_by('-data_movimentacao')
            
            movimentacoes_data = []
            for mov in movimentacoes:
                movimentacoes_data.append({
                    'id': mov.id,
                    'tipo': mov.tipo,
                    'quantidade': mov.quantidade,
                    'motivo': mov.motivo,
                    'referencia': mov.referencia,
                    'data_movimentacao': mov.data_movimentacao.isoformat(),
                    'data_formatada': mov.data_movimentacao.strftime('%d/%m/%Y %H:%M'),
                    'usuario': mov.usuario.username if mov.usuario else 'Sistema'
                })
            
            return JsonResponse({
                'success': True,
                'produto_id': produto.id,
                'produto_nome': produto.nome_produto,
                'movimentacoes': movimentacoes_data
            })
            
        except CadastroTipoProduto.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Produto não encontrado'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })
    
class DeleteCadastroTipoProdutoView(DeleteView):
    model = CadastroTipoProduto
    success_url = reverse_lazy('cadastro_tipo_produto')
    
    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            produto_nome = self.object.nome_produto
            self.object.delete()
            return JsonResponse({
                'success': True,
                'message': f'Produto "{produto_nome}" excluído com sucesso!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao excluir produto: {str(e)}'
            })

class DeleteEntradaProdutoView(DeleteView):
    model = EntradaProduto
    success_url = reverse_lazy('entrada_produto')
    
    def delete(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info(f"DELETE - Request recebido para entrada {kwargs.get('pk')}")
        produtos_logger.info(f"DELETE - Method: {request.method}")
        
        try:
            self.object = self.get_object()
            produtos_logger.info(f"DELETE - Entrada encontrada: ID {self.object.id}")
            produtos_logger.info(f"DELETE - Produto: {self.object.codigo_produto.nome_produto}")
            produtos_logger.info(f"DELETE - Quantidade: {self.object.quantidade}")
            produtos_logger.info(f"DELETE - ID equipamento: {self.object.id_equipamento}")
            
            entrada_info = f"{self.object.codigo_produto.nome_produto} - Qtd: {self.object.quantidade} - ID: {self.object.id_equipamento}"
            
            # Verificar se existem outras entradas com o mesmo ID de equipamento
            entradas_mesmo_id = EntradaProduto.objects.filter(
                id_equipamento=self.object.id_equipamento
            ).exclude(id=self.object.id)
            
            produtos_logger.info(f"DELETE - Entradas com mesmo ID: {entradas_mesmo_id.count()}")
            
            # Deletar a entrada
            self.object.delete()
            produtos_logger.info("DELETE - Entrada deletada com sucesso")
            
            # Mensagem informativa sobre outras entradas
            mensagem = f'Entrada "{entrada_info}" excluída com sucesso!'
            if entradas_mesmo_id.exists():
                mensagem += f' (Ainda existem {entradas_mesmo_id.count()} outras entradas com o ID {self.object.id_equipamento})'
                produtos_logger.warning(f"DELETE - Aviso: {entradas_mesmo_id.count()} entradas restantes com mesmo ID")
            
            response_data = {
                'success': True,
                'message': mensagem,
                'remaining_entries': entradas_mesmo_id.count() if entradas_mesmo_id.exists() else 0
            }
            
            produtos_logger.info(f"DELETE - Response preparada com sucesso")
            produtos_logger.info("=" * 50)
            return JsonResponse(response_data)
            
        except Exception as e:
            produtos_logger.error(f"DELETE - Erro ao excluir entrada: {str(e)}")
            produtos_logger.error(f"DELETE - Tipo do erro: {type(e)}")
            import traceback
            produtos_logger.error(f"DELETE - Traceback: {traceback.format_exc()}")
            produtos_logger.info("=" * 50)
            return JsonResponse({
                'success': False,
                'message': f'Erro ao excluir entrada: {str(e)}'
            })
    
class ListCadastroTipoProdutoView(ListView):
    model = CadastroTipoProduto
    template_name = 'produtos/listagem_produtos.html'
    context_object_name = 'object_list'
    paginate_by = 20
    
    def get(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info("GET - ListCadastroTipoProdutoView (Lista) iniciado")
        produtos_logger.info(f"GET - Request path: {request.path}")
        produtos_logger.info(f"GET - User: {request.user}")
        
        try:
            response = super().get(request, *args, **kwargs)
            produtos_logger.info(f"GET - Lista de produtos carregada com {len(response.context_data['object_list'])} produtos")
            produtos_logger.info("=" * 50)
            return response
        except Exception as e:
            produtos_logger.error(f"GET - Erro ao carregar lista de produtos: {e}")
            produtos_logger.info("=" * 50)
            raise

class ListEntradaProdutoView(ListView):
    model = EntradaProduto
    template_name = 'produtos/listagem_entradas.html'
    context_object_name = 'object_list'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = CadastroTipoProduto.objects.all()
        return context

class DetailCadastroTipoProdutoView(DetailView):
    model = CadastroTipoProduto
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return JsonResponse({
            'id': self.object.id,
            'nome_produto': self.object.nome_produto,
            'descricao': self.object.descricao,
            'fabricante': self.object.fabricante,
            'telefone_fabricante': self.object.telefone_fabricante or '',
            'email_fabricante': self.object.email_fabricante or '',
            'valor_unitario': str(self.object.valor_unitario) if self.object.valor_unitario else '0.00',
            'data_cadastro': self.object.data_cadastro.strftime('%d/%m/%Y')
        })

class DetailEntradaProdutoView(DetailView):
    model = EntradaProduto
    
    def get(self, request, *args, **kwargs):
        produtos_logger.info("=" * 50)
        produtos_logger.info("GET - DetailEntradaProdutoView iniciado")
        produtos_logger.info(f"GET - Request path: {request.path}")
        produtos_logger.info(f"GET - Entrada ID solicitada: {kwargs.get('pk')}")
        
        try:
            self.object = self.get_object()
            produtos_logger.info(f"GET - Objeto encontrado: ID {self.object.id}")
            produtos_logger.info(f"GET - Produto: {self.object.codigo_produto.nome_produto}")
            produtos_logger.info(f"GET - Quantidade: {self.object.quantidade}")
            produtos_logger.info(f"GET - ID equipamento: {self.object.id_equipamento}")
            produtos_logger.info(f"GET - Total de IDs: {len(self.object.get_ids_equipamentos_list())}")
            
            # Testar métodos do modelo
            try:
                total_ids = self.object.get_quantidade_ids()
                produtos_logger.info(f"GET - Total IDs calculado: {total_ids}")
            except Exception as e:
                produtos_logger.error(f"GET - Erro no get_quantidade_ids(): {e}")
                total_ids = 1
            
            try:
                historico_ids = self.object.get_historico_ids()
                produtos_logger.info(f"GET - Histórico IDs obtido: {len(historico_ids)} registros")
            except Exception as e:
                produtos_logger.error(f"GET - Erro no get_historico_ids(): {e}")
                historico_ids = []
        
            # Preparar resposta
            response_data = {
                'id': self.object.id,
                'codigo_produto': {
                    'id': self.object.codigo_produto.id,
                    'nome_produto': self.object.codigo_produto.nome_produto
                },
                'quantidade': self.object.quantidade,
                'id_equipamento': self.object.id_equipamento,
                'data': self.object.data.strftime('%Y-%m-%dT%H:%M'),
                'valor_nota': str(self.object.valor_nota) if self.object.valor_nota else '0.00',
                'numero_nota_fiscal': self.object.numero_nota_fiscal,
                'data_entrada': self.object.data_entrada.strftime('%d/%m/%Y %H:%M'),
                'total_ids': total_ids,
                'historico_ids': historico_ids
            }
            
            produtos_logger.info(f"GET - Response preparada com sucesso")
            produtos_logger.info("=" * 50)
            
            return JsonResponse(response_data)
            
        except Exception as e:
            produtos_logger.error(f"GET - Erro geral na view: {e}")
            produtos_logger.error(f"GET - Tipo do erro: {type(e)}")
            import traceback
            produtos_logger.error(f"GET - Traceback: {traceback.format_exc()}")
            produtos_logger.info("=" * 50)
            
            return JsonResponse({
                'error': True,
                'message': f'Erro ao carregar detalhes: {str(e)}',
                'debug_info': {
                    'error_type': str(type(e)),
                    'error_message': str(e)
                }
            }, status=500)

class BuscarEquipamentoView(View):
    """View para buscar equipamento por ID"""
    
    def get(self, request):
        id_equipamento = request.GET.get('id_equipamento', '').strip()
        
        if not id_equipamento:
            return JsonResponse({
                'success': False,
                'message': 'ID do equipamento é obrigatório'
            })
        
        # Buscar entradas que contenham este ID de equipamento
        entradas = EntradaProduto.objects.filter(
            models.Q(id_equipamento__icontains=id_equipamento) |
            models.Q(ids_equipamentos__icontains=id_equipamento)
        ).order_by('-data_entrada')
        
        if entradas.exists():
            # Equipamento encontrado
            equipamento_info = []
            total_quantidade = 0
            
            for entrada in entradas:
                # Verificar se o ID está na lista de IDs
                ids_list = entrada.get_ids_equipamentos_list()
                if id_equipamento in ids_list:
                    equipamento_info.append({
                        'id': entrada.id,
                        'produto': entrada.codigo_produto.nome_produto,
                        'quantidade': entrada.quantidade,
                        'data_entrada': entrada.data_entrada.strftime('%d/%m/%Y %H:%M'),
                        'data': entrada.data.strftime('%d/%m/%Y %H:%M'),
                        'numero_nota_fiscal': entrada.numero_nota_fiscal,
                        'valor_nota': str(entrada.valor_nota) if entrada.valor_nota else '0.00',
                        'total_ids': entrada.get_quantidade_ids()
                    })
                    total_quantidade += entrada.quantidade
            
            return JsonResponse({
                'success': True,
                'encontrado': True,
                'id_equipamento': id_equipamento,
                'total_quantidade': total_quantidade,
                'total_entradas': len(equipamento_info),
                'equipamento_info': equipamento_info,
                'message': f'Equipamento {id_equipamento} encontrado em {len(equipamento_info)} entrada(s) com total de {total_quantidade} unidades'
            })
        else:
            # Equipamento não encontrado
            return JsonResponse({
                'success': True,
                'encontrado': False,
                'id_equipamento': id_equipamento,
                'message': f'Equipamento {id_equipamento} não foi encontrado no estoque'
            })

@method_decorator(csrf_exempt, name='dispatch')
class CadastroProdutoModalView(CreateView):
    """View para cadastro de produto via modal"""
    model = CadastroTipoProduto
    form_class = CadastroTipoProdutoForm
    
    def post(self, request, *args, **kwargs):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                produto = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Produto cadastrado com sucesso!',
                    'produto': {
                        'id': produto.id,
                        'nome_produto': produto.nome_produto,
                        'fabricante': produto.fabricante,
                        'valor_unitario': str(produto.valor_unitario) if produto.valor_unitario else '0.00'
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Erro no formulário',
                    'errors': form.errors
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

class EstoqueView(ListView):
    """View para exibir o estoque disponível de todos os produtos"""
    model = CadastroTipoProduto
    template_name = 'produtos/estoque.html'
    context_object_name = 'produtos'
    paginate_by = 20
    
    def get_queryset(self):
        """Retorna produtos com informações de estoque"""
        produtos = CadastroTipoProduto.objects.all()
        
        # Adicionar informações de estoque para cada produto
        for produto in produtos:
            produto.estoque_disponivel = produto.get_estoque_disponivel()
            produto.total_entradas = MovimentacaoEstoque.objects.filter(
                produto=produto, tipo='entrada'
            ).aggregate(total=models.Sum('quantidade'))['total'] or 0
            produto.total_saidas = MovimentacaoEstoque.objects.filter(
                produto=produto, tipo='saida'
            ).aggregate(total=models.Sum('quantidade'))['total'] or 0
        
        return produtos
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Controle de Estoque'
        context['active_tab'] = 'estoque'
        return context

@method_decorator(csrf_exempt, name='dispatch')
class EstoqueAPIView(View):
    """API para consultar estoque de um produto específico"""
    
    def get(self, request, produto_id):
        try:
            produto = CadastroTipoProduto.objects.get(id=produto_id)
            estoque_disponivel = produto.get_estoque_disponivel()
            
            return JsonResponse({
                'success': True,
                'produto_id': produto.id,
                'produto_nome': produto.nome_produto,
                'estoque_disponivel': estoque_disponivel
            })
            
        except CadastroTipoProduto.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Produto não encontrado'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })

@method_decorator(csrf_exempt, name='dispatch')
class MovimentacoesAPIView(View):
    """API para buscar movimentações de um produto específico"""
    
    def get(self, request, produto_id):
        try:
            produto = CadastroTipoProduto.objects.get(id=produto_id)
            movimentacoes = MovimentacaoEstoque.objects.filter(produto=produto).order_by('-data_movimentacao')
            
            movimentacoes_data = []
            for mov in movimentacoes:
                movimentacoes_data.append({
                    'id': mov.id,
                    'tipo': mov.tipo,
                    'quantidade': mov.quantidade,
                    'motivo': mov.motivo,
                    'referencia': mov.referencia,
                    'data_movimentacao': mov.data_movimentacao.isoformat(),
                    'data_formatada': mov.data_movimentacao.strftime('%d/%m/%Y %H:%M'),
                    'usuario': mov.usuario.username if mov.usuario else 'Sistema'
                })
            
            return JsonResponse({
                'success': True,
                'produto_id': produto.id,
                'produto_nome': produto.nome_produto,
                'movimentacoes': movimentacoes_data
            })
            
        except CadastroTipoProduto.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Produto não encontrado'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            })
    
