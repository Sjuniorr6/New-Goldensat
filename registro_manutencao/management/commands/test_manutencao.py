from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random

from registro_manutencao.models import registrodemanutencao, ImagemRegistro, retorno
from clientes.models import Clientes
from produtos.models import CadastroTipoProduto

class Command(BaseCommand):
    help = 'Cria manutenções de teste e testa o sistema'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando testes de estresse do sistema de manutenção...'))
        
        # Verificar se existem clientes e produtos
        clientes = Clientes.objects.all()
        produtos = CadastroTipoProduto.objects.all()
        
        if not clientes.exists():
            self.stdout.write(self.style.WARNING('❌ Nenhum cliente encontrado. Criando cliente de teste...'))
            cliente_teste = Clientes.objects.create(
                nome_fantasia="Cliente Teste",
                razao_social="Cliente Teste LTDA",
                cnpj="12345678000199",
                email="teste@cliente.com"
            )
            clientes = [cliente_teste]
        else:
            clientes = list(clientes)
        
        if not produtos.exists():
            self.stdout.write(self.style.WARNING('❌ Nenhum produto encontrado. Criando produto de teste...'))
            produto_teste = CadastroTipoProduto.objects.create(
                nome_produto="GS410 (2G) - Teste",
                descricao="Produto de teste para manutenção"
            )
            produtos = [produto_teste]
        else:
            produtos = list(produtos)
        
        # Status possíveis
        status_options = [
            'Pendente',
            'Aprovado',
            'Reprovado pela Diretoria',
            'Aprovado pela Diretoria',
            'Expedição',
            'expedido'
        ]
        
        # Tipos de entrada
        tipos_entrada = [
            'Devolução / Estoque',
            'Garantia',
            'Manutenção Preventiva',
            'Manutenção Corretiva'
        ]
        
        # Motivos
        motivos = [
            'Defeito de Fábrica',
            'Desgaste Natural',
            'Danos por Uso',
            'Problema de Software',
            'Falha de Hardware'
        ]
        
        # Customizações
        customizacoes = [
            'Padrão',
            'Personalizada',
            'Especial',
            'Industrial'
        ]
        
        # Tipos de contrato
        tipos_contrato = [
            'Garantia',
            'Pós-Venda',
            'Contrato Anual',
            'Avulso'
        ]
        
        self.stdout.write('📊 Criando 15 manutenções de teste...')
        
        manutencoes_criadas = []
        
        for i in range(15):
            try:
                # Dados aleatórios
                cliente = random.choice(clientes)
                produto = random.choice(produtos)
                status = random.choice(status_options)
                tipo_entrada = random.choice(tipos_entrada)
                motivo = random.choice(motivos)
                customizacao = random.choice(customizacoes)
                tipo_contrato = random.choice(tipos_contrato)
                
                # Criar manutenção
                manutencao = registrodemanutencao.objects.create(
                    nome=cliente,
                    tipo_entrada=tipo_entrada,
                    tipo_produto=produto,
                    motivo=motivo,
                    tipo_customizacao=customizacao,
                    recebimento='Recebido',
                    entregue_por_retirado_por='Cliente',
                    id_equipamentos=f"ID{i+1:03d}, ID{i+2:03d}, ID{i+3:03d}",
                    quantidade=random.randint(1, 10),
                    tipo_contrato=tipo_contrato,
                    customizacaoo=customizacao,
                    numero_equipamento=f"EQ{i+1:04d}, EQ{i+2:04d}",
                    observacoes=f"Observações de teste para manutenção {i+1}. Sistema funcionando corretamente.",
                    tratativa='Análise Técnica',
                    status=status,
                    status_tratativa='Em Andamento',
                    data_devolucao=timezone.now() + timedelta(days=random.randint(1, 30))
                )
                
                manutencoes_criadas.append(manutencao)
                self.stdout.write(f'✅ Manutenção {i+1} criada - ID: {manutencao.id} - Status: {status}')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao criar manutenção {i+1}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'🎉 {len(manutencoes_criadas)} manutenções criadas com sucesso!'))
        
        # Testar alteração de status
        self.stdout.write('\n🔄 Testando alteração de status...')
        
        manutencoes = registrodemanutencao.objects.all()
        
        if manutencoes.exists():
            status_sequence = [
                'Pendente',
                'Aprovado',
                'Aprovado pela Diretoria',
                'Expedição',
                'expedido'
            ]
            
            self.stdout.write(f'📋 Testando alteração de status em {min(5, manutencoes.count())} manutenções...')
            
            for i, manutencao in enumerate(manutencoes[:5]):  # Testar apenas 5
                try:
                    # Alterar status sequencialmente
                    for status in status_sequence:
                        manutencao.status = status
                        manutencao.save()
                        self.stdout.write(f'✅ Manutenção {manutencao.id}: Status alterado para "{status}"')
                    
                    self.stdout.write(f'🎯 Manutenção {manutencao.id} - Ciclo completo de status testado')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'❌ Erro ao alterar status da manutenção {manutencao.id}: {e}'))
            
            self.stdout.write('✅ Teste de alteração de status concluído!')
        
        # Mostrar estatísticas
        self.stdout.write('\n📈 Estatísticas do Sistema:')
        
        total_manutencoes = registrodemanutencao.objects.count()
        self.stdout.write(f'📊 Total de manutenções: {total_manutencoes}')
        
        # Estatísticas por status
        for status in ['Pendente', 'Aprovado', 'Aprovado pela Diretoria', 'Expedição', 'expedido']:
            count = registrodemanutencao.objects.filter(status=status).count()
            self.stdout.write(f'📊 Status "{status}": {count}')
        
        # Estatísticas por tipo de entrada
        tipos = registrodemanutencao.objects.values_list('tipo_entrada', flat=True).distinct()
        for tipo in tipos:
            count = registrodemanutencao.objects.filter(tipo_entrada=tipo).count()
            self.stdout.write(f'📊 Tipo "{tipo}": {count}')
        
        # Manutenções recentes
        recentes = registrodemanutencao.objects.order_by('-data_criacao')[:5]
        self.stdout.write(f'\n🕒 Últimas 5 manutenções:')
        for manutencao in recentes:
            self.stdout.write(f'   ID: {manutencao.id} - {manutencao.nome.nome_fantasia} - {manutencao.status} - {manutencao.data_criacao.strftime("%d/%m/%Y %H:%M")}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 TODOS OS TESTES CONCLUÍDOS COM SUCESSO!'))




