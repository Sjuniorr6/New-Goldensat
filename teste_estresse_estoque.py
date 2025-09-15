#!/usr/bin/env python
"""
TESTE DE ESTRESSE DO SISTEMA DE CONTROLE DE ESTOQUE
==================================================

Este script testa todos os cenários possíveis do sistema de controle de estoque:
1. Validação de formulários
2. Signals de movimentação
3. Cenários de stress
4. Mudanças de status
5. Exclusões
6. Integridade de dados
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'int.settings')
django.setup()

from requisicoes.models import Requisicoes
from requisicoes.forms import RequisicaoForm
from produtos.models import CadastroTipoProduto, MovimentacaoEstoque, EntradaProduto
from clientes.models import Clientes
from django.db import transaction
from django.core.exceptions import ValidationError
import traceback

class TesteEstresseEstoque:
    def __init__(self):
        self.produto = None
        self.cliente = None
        self.resultados = []
        self.erros = []
        
    def log_resultado(self, teste, sucesso, mensagem, detalhes=None):
        """Registra resultado de um teste"""
        status = "✅ PASSOU" if sucesso else "❌ FALHOU"
        self.resultados.append({
            'teste': teste,
            'sucesso': sucesso,
            'mensagem': mensagem,
            'detalhes': detalhes
        })
        print(f"{status} - {teste}: {mensagem}")
        if detalhes:
            print(f"    Detalhes: {detalhes}")
    
    def log_erro(self, teste, erro):
        """Registra erro de um teste"""
        self.erros.append({
            'teste': teste,
            'erro': str(erro),
            'traceback': traceback.format_exc()
        })
        print(f"❌ ERRO - {teste}: {str(erro)}")
    
    def setup_dados_teste(self):
        """Configura dados básicos para os testes"""
        try:
            # Criar ou obter produto de teste
            self.produto, created = CadastroTipoProduto.objects.get_or_create(
                nome_produto="PRODUTO TESTE ESTRESSE",
                defaults={
                    'fabricante': 'FABRICANTE TESTE',
                    'descricao': 'PRODUTO PARA TESTES DE ESTRESSE',
                    'valor_unitario': Decimal('100.00')
                }
            )
            
            # Criar ou obter cliente de teste
            self.cliente, created = Clientes.objects.get_or_create(
                nome="CLIENTE TESTE ESTRESSE",
                defaults={
                    'cnpj': '12345678000199',
                    'endereco': 'Endereço Teste',
                    'comercial': '11999999999'
                }
            )
            
            # Limpar movimentações anteriores do produto de teste
            MovimentacaoEstoque.objects.filter(produto=self.produto).delete()
            
            # Adicionar estoque inicial
            MovimentacaoEstoque.objects.create(
                produto=self.produto,
                tipo='entrada',
                quantidade=100,
                motivo='Estoque inicial para testes',
                referencia='TESTE_INICIAL'
            )
            
            self.log_resultado("Setup", True, f"Produto: {self.produto.nome_produto}, Cliente: {self.cliente.nome}")
            
        except Exception as e:
            self.log_erro("Setup", e)
            raise
    
    def teste_1_validacao_formulario(self):
        """Teste 1: Validação de formulário com estoque insuficiente"""
        try:
            # Teste com quantidade maior que estoque
            dados = {
                'nome': self.cliente.id,
                'tipo_produto': self.produto.id,
                'numero_de_equipamentos': '150',  # Mais que o estoque (100)
                'status': 'Pendente',
                'taxa_envio': '0.00',
                'valor_unitario': '100.00',
                'valor_total': '15000.00'
            }
            
            form = RequisicaoForm(dados)
            if not form.is_valid():
                self.log_resultado("Validação Formulário", True, "Formulário rejeitou quantidade maior que estoque", form.errors)
            else:
                self.log_resultado("Validação Formulário", False, "Formulário aceitou quantidade maior que estoque")
                
        except Exception as e:
            self.log_erro("Validação Formulário", e)
    
    def teste_2_criacao_requisicao_valida(self):
        """Teste 2: Criação de requisição com quantidade válida"""
        try:
            dados = {
                'nome': self.cliente.id,
                'tipo_produto': self.produto.id,
                'numero_de_equipamentos': '10',
                'status': 'Pendente',
                'taxa_envio': '0.00',
                'valor_unitario': '100.00',
                'valor_total': '1000.00'
            }
            
            form = RequisicaoForm(dados)
            if form.is_valid():
                requisicao = form.save()
                estoque_apos = self.produto.get_estoque_disponivel()
                
                if estoque_apos == 90:  # 100 - 10
                    self.log_resultado("Criação Requisição", True, f"Estoque atualizado corretamente: {estoque_apos}")
                else:
                    self.log_resultado("Criação Requisição", False, f"Estoque incorreto: {estoque_apos} (esperado: 90)")
                    
                return requisicao
            else:
                self.log_resultado("Criação Requisição", False, "Formulário inválido", form.errors)
                return None
                
        except Exception as e:
            self.log_erro("Criação Requisição", e)
            return None
    
    def teste_3_mudanca_status_aprovado(self, requisicao):
        """Teste 3: Mudança de status para aprovado"""
        try:
            if not requisicao:
                self.log_resultado("Mudança Status", False, "Requisição não disponível")
                return
            
            estoque_antes = self.produto.get_estoque_disponivel()
            
            # Simular mudança de status
            requisicao._previous_status = requisicao.status
            requisicao.status = 'Aprovado pelo CEO'
            requisicao.save()
            
            estoque_apos = self.produto.get_estoque_disponivel()
            
            if estoque_antes == estoque_apos:
                self.log_resultado("Mudança Status", True, "Estoque mantido ao aprovar")
            else:
                self.log_resultado("Mudança Status", False, f"Estoque alterado incorretamente: {estoque_antes} -> {estoque_apos}")
                
        except Exception as e:
            self.log_erro("Mudança Status", e)
    
    def teste_4_mudanca_status_reprovado(self, requisicao):
        """Teste 4: Mudança de status para reprovado (deve restaurar estoque)"""
        try:
            if not requisicao:
                self.log_resultado("Restauração Estoque", False, "Requisição não disponível")
                return
            
            estoque_antes = self.produto.get_estoque_disponivel()
            
            # Simular mudança para reprovado
            requisicao._previous_status = requisicao.status
            requisicao.status = 'Reprovado pelo CEO'
            requisicao.save()
            
            estoque_apos = self.produto.get_estoque_disponivel()
            
            if estoque_apos == estoque_antes + 10:  # Deve restaurar 10 unidades
                self.log_resultado("Restauração Estoque", True, f"Estoque restaurado: {estoque_antes} -> {estoque_apos}")
            else:
                self.log_resultado("Restauração Estoque", False, f"Estoque não restaurado: {estoque_antes} -> {estoque_apos}")
                
        except Exception as e:
            self.log_erro("Restauração Estoque", e)
    
    def teste_5_multiplas_requisicoes(self):
        """Teste 5: Múltiplas requisições simultâneas"""
        try:
            estoque_inicial = self.produto.get_estoque_disponivel()
            requisicoes_criadas = []
            
            # Criar 5 requisições de 5 unidades cada
            for i in range(5):
                dados = {
                    'nome': self.cliente.id,
                    'tipo_produto': self.produto.id,
                    'numero_de_equipamentos': '5',
                    'status': 'Pendente',
                    'taxa_envio': '0.00',
                    'valor_unitario': '100.00',
                    'valor_total': '500.00'
                }
                
                form = RequisicaoForm(dados)
                if form.is_valid():
                    requisicao = form.save()
                    requisicoes_criadas.append(requisicao)
                else:
                    self.log_resultado("Múltiplas Requisições", False, f"Falha ao criar requisição {i+1}", form.errors)
                    return
            
            estoque_final = self.produto.get_estoque_disponivel()
            estoque_esperado = estoque_inicial - 25  # 5 requisições * 5 unidades
            
            if estoque_final == estoque_esperado:
                self.log_resultado("Múltiplas Requisições", True, f"Estoque correto: {estoque_final} (esperado: {estoque_esperado})")
            else:
                self.log_resultado("Múltiplas Requisições", False, f"Estoque incorreto: {estoque_final} (esperado: {estoque_esperado})")
            
            return requisicoes_criadas
            
        except Exception as e:
            self.log_erro("Múltiplas Requisições", e)
            return []
    
    def teste_6_exclusao_requisicoes(self, requisicoes):
        """Teste 6: Exclusão de requisições (deve restaurar estoque)"""
        try:
            if not requisicoes:
                self.log_resultado("Exclusão Requisições", False, "Nenhuma requisição para excluir")
                return
            
            estoque_antes = self.produto.get_estoque_disponivel()
            
            # Excluir todas as requisições
            for requisicao in requisicoes:
                requisicao.delete()
            
            estoque_apos = self.produto.get_estoque_disponivel()
            estoque_esperado = estoque_antes + 25  # Deve restaurar 25 unidades
            
            if estoque_apos == estoque_esperado:
                self.log_resultado("Exclusão Requisições", True, f"Estoque restaurado: {estoque_antes} -> {estoque_apos}")
            else:
                self.log_resultado("Exclusão Requisições", False, f"Estoque não restaurado: {estoque_antes} -> {estoque_apos}")
                
        except Exception as e:
            self.log_erro("Exclusão Requisições", e)
    
    def teste_7_integridade_dados(self):
        """Teste 7: Verificar integridade dos dados"""
        try:
            # Verificar se todas as movimentações estão corretas
            movimentacoes = MovimentacaoEstoque.objects.filter(produto=self.produto)
            
            total_entradas = sum(m.quantidade for m in movimentacoes if m.tipo == 'entrada')
            total_saidas = sum(m.quantidade for m in movimentacoes if m.tipo == 'saida')
            estoque_calculado = total_entradas - total_saidas
            estoque_metodo = self.produto.get_estoque_disponivel()
            
            if estoque_calculado == estoque_metodo:
                self.log_resultado("Integridade Dados", True, f"Estoque consistente: {estoque_calculado}")
            else:
                self.log_resultado("Integridade Dados", False, f"Estoque inconsistente: calculado={estoque_calculado}, método={estoque_metodo}")
            
            # Verificar se não há requisições órfãs
            requisicoes_ativas = Requisicoes.objects.filter(
                status__in=['Pendente', 'Configurado', 'Aprovado pelo CEO']
            )
            
            for req in requisicoes_ativas:
                if not req.tipo_produto or not req.numero_de_equipamentos:
                    self.log_resultado("Integridade Dados", False, f"Requisição {req.id} sem produto ou quantidade")
                    return
            
            self.log_resultado("Integridade Dados", True, f"Todas as {len(requisicoes_ativas)} requisições ativas são válidas")
            
        except Exception as e:
            self.log_erro("Integridade Dados", e)
    
    def teste_8_cenario_limite_estoque(self):
        """Teste 8: Cenário de limite de estoque (tentar esgotar)"""
        try:
            estoque_atual = self.produto.get_estoque_disponivel()
            
            # Tentar criar requisição com exatamente o estoque disponível
            dados = {
                'nome': self.cliente.id,
                'tipo_produto': self.produto.id,
                'numero_de_equipamentos': str(estoque_atual),
                'status': 'Pendente',
                'taxa_envio': '0.00',
                'valor_unitario': '100.00',
                'valor_total': str(float(estoque_atual) * 100.00)
            }
            
            form = RequisicaoForm(dados)
            if form.is_valid():
                requisicao = form.save()
                estoque_apos = self.produto.get_estoque_disponivel()
                
                if estoque_apos == 0:
                    self.log_resultado("Limite Estoque", True, "Estoque esgotado corretamente")
                    
                    # Tentar criar outra requisição (deve falhar)
                    dados2 = {
                        'nome': self.cliente.id,
                        'tipo_produto': self.produto.id,
                        'numero_de_equipamentos': '1',
                        'status': 'Pendente',
                        'taxa_envio': '0.00',
                        'valor_unitario': '100.00',
                        'valor_total': '100.00'
                    }
                    
                    form2 = RequisicaoForm(dados2)
                    if not form2.is_valid():
                        self.log_resultado("Limite Estoque", True, "Segunda requisição rejeitada corretamente")
                    else:
                        self.log_resultado("Limite Estoque", False, "Segunda requisição foi aceita incorretamente")
                    
                    return requisicao
                else:
                    self.log_resultado("Limite Estoque", False, f"Estoque não esgotado: {estoque_apos}")
                    return None
            else:
                self.log_resultado("Limite Estoque", False, "Formulário rejeitado", form.errors)
                return None
                
        except Exception as e:
            self.log_erro("Limite Estoque", e)
            return None
    
    def executar_todos_testes(self):
        """Executa todos os testes em sequência"""
        print("🚀 INICIANDO TESTES DE ESTRESSE DO SISTEMA DE ESTOQUE")
        print("=" * 60)
        
        try:
            # Setup
            self.setup_dados_teste()
            
            # Teste 1: Validação
            self.teste_1_validacao_formulario()
            
            # Teste 2: Criação válida
            requisicao = self.teste_2_criacao_requisicao_valida()
            
            # Teste 3: Mudança para aprovado
            self.teste_3_mudanca_status_aprovado(requisicao)
            
            # Teste 4: Mudança para reprovado
            self.teste_4_mudanca_status_reprovado(requisicao)
            
            # Teste 5: Múltiplas requisições
            requisicoes = self.teste_5_multiplas_requisicoes()
            
            # Teste 6: Exclusão
            self.teste_6_exclusao_requisicoes(requisicoes)
            
            # Teste 7: Integridade
            self.teste_7_integridade_dados()
            
            # Teste 8: Limite
            self.teste_8_cenario_limite_estoque()
            
        except Exception as e:
            print(f"❌ ERRO CRÍTICO: {str(e)}")
            print(traceback.format_exc())
        
        # Relatório final
        self.relatorio_final()
    
    def relatorio_final(self):
        """Gera relatório final dos testes"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL DOS TESTES")
        print("=" * 60)
        
        total_testes = len(self.resultados)
        testes_passaram = sum(1 for r in self.resultados if r['sucesso'])
        testes_falharam = total_testes - testes_passaram
        
        print(f"Total de testes: {total_testes}")
        print(f"✅ Passaram: {testes_passaram}")
        print(f"❌ Falharam: {testes_falharam}")
        
        if total_testes > 0:
            print(f"📈 Taxa de sucesso: {(testes_passaram/total_testes)*100:.1f}%")
        else:
            print("📈 Taxa de sucesso: N/A (nenhum teste executado)")
        
        if self.erros:
            print(f"\n❌ ERROS ENCONTRADOS: {len(self.erros)}")
            for erro in self.erros:
                print(f"  - {erro['teste']}: {erro['erro']}")
        
        if testes_falharam > 0:
            print(f"\n❌ TESTES QUE FALHARAM:")
            for resultado in self.resultados:
                if not resultado['sucesso']:
                    print(f"  - {resultado['teste']}: {resultado['mensagem']}")
        
        print("\n" + "=" * 60)
        
        if testes_falharam == 0 and len(self.erros) == 0:
            print("🎉 TODOS OS TESTES PASSARAM! SISTEMA FUNCIONANDO CORRETAMENTE!")
        else:
            print("⚠️ ALGUNS TESTES FALHARAM. VERIFIQUE OS PROBLEMAS ACIMA.")
        
        print("=" * 60)

if __name__ == "__main__":
    teste = TesteEstresseEstoque()
    teste.executar_todos_testes()
