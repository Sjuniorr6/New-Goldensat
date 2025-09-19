from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from registro_manutencao.models import registrodemanutencao
from clientes.models import Clientes
from produtos.models import CadastroTipoProduto

class Command(BaseCommand):
    help = 'Cria 20 registros de manutenção para teste'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Criando 20 registros de manutenção para teste...'))
        
        # Verificar se existem clientes e produtos
        clientes = Clientes.objects.all()
        produtos = CadastroTipoProduto.objects.all()
        
        if not clientes.exists():
            self.stdout.write(self.style.WARNING('❌ Nenhum cliente encontrado. Criando clientes de teste...'))
            clientes_teste = [
                Clientes.objects.create(
                    nome_fantasia="COIMPA INDUSTRIAL LTDA",
                    razao_social="COIMPA INDUSTRIAL LTDA",
                    cnpj="12345678000199",
                    email="contato@coimpa.com"
                ),
                Clientes.objects.create(
                    nome_fantasia="TECH SOLUTIONS BR",
                    razao_social="TECH SOLUTIONS BRASIL LTDA",
                    cnpj="98765432000188",
                    email="contato@techsolutions.com"
                ),
                Clientes.objects.create(
                    nome_fantasia="INDUSTRIAL CORP",
                    razao_social="INDUSTRIAL CORPORATION LTDA",
                    cnpj="11223344000177",
                    email="contato@industrial.com"
                ),
                Clientes.objects.create(
                    nome_fantasia="AUTOMATION PRO",
                    razao_social="AUTOMATION PROFESSIONAL LTDA",
                    cnpj="55667788000166",
                    email="contato@automation.com"
                ),
                Clientes.objects.create(
                    nome_fantasia="DIGITAL SYSTEMS",
                    razao_social="DIGITAL SYSTEMS LTDA",
                    cnpj="99887766000155",
                    email="contato@digital.com"
                )
            ]
            clientes = clientes_teste
        else:
            clientes = list(clientes)
        
        if not produtos.exists():
            self.stdout.write(self.style.WARNING('❌ Nenhum produto encontrado. Criando produtos de teste...'))
            produtos_teste = [
                CadastroTipoProduto.objects.create(
                    nome_produto="GS410 (2G)",
                    descricao="Gateway GS410 2G"
                ),
                CadastroTipoProduto.objects.create(
                    nome_produto="GS410 (4G)",
                    descricao="Gateway GS410 4G"
                ),
                CadastroTipoProduto.objects.create(
                    nome_produto="GS420 (2G)",
                    descricao="Gateway GS420 2G"
                ),
                CadastroTipoProduto.objects.create(
                    nome_produto="GS420 (4G)",
                    descricao="Gateway GS420 4G"
                ),
                CadastroTipoProduto.objects.create(
                    nome_produto="GS430 (4G)",
                    descricao="Gateway GS430 4G"
                )
            ]
            produtos = produtos_teste
        else:
            produtos = list(produtos)
        
        # Dados para os registros
        status_options = [
            'Pendente',
            'Aprovado',
            'Reprovado pela Diretoria',
            'Aprovado pela Diretoria',
            'Expedição',
            'expedido'
        ]
        
        tipos_entrada = [
            'Devolução / Estoque',
            'Garantia',
            'Manutenção Preventiva',
            'Manutenção Corretiva',
            'Retorno de Campo',
            'Teste de Qualidade'
        ]
        
        motivos = [
            'Defeito de Fábrica',
            'Desgaste Natural',
            'Danos por Uso',
            'Problema de Software',
            'Falha de Hardware',
            'Atualização de Firmware',
            'Calibração',
            'Limpeza e Manutenção'
        ]
        
        customizacoes = [
            'Padrão',
            'Personalizada',
            'Especial',
            'Industrial',
            'Marítima',
            'Automotiva'
        ]
        
        tipos_contrato = [
            'Garantia',
            'Pós-Venda',
            'Contrato Anual',
            'Avulso',
            'Manutenção Preventiva',
            'Suporte Técnico'
        ]
        
        tratativas = [
            'Análise Técnica',
            'Teste de Funcionamento',
            'Substituição de Peças',
            'Atualização de Software',
            'Calibração',
            'Limpeza',
            'Reparo',
            'Substituição Completa'
        ]
        
        status_tratativas = [
            'Em Andamento',
            'Concluída',
            'Aguardando Peças',
            'Aguardando Aprovação',
            'Cancelada'
        ]
        
        entregue_por_options = [
            'Cliente',
            'Técnico de Campo',
            'Transportadora',
            'Representante',
            'Equipe Interna'
        ]
        
        self.stdout.write('📊 Criando registros...')
        
        manutencoes_criadas = []
        
        for i in range(20):
            try:
                # Dados aleatórios
                cliente = random.choice(clientes)
                produto = random.choice(produtos)
                status = random.choice(status_options)
                tipo_entrada = random.choice(tipos_entrada)
                motivo = random.choice(motivos)
                customizacao = random.choice(customizacoes)
                tipo_contrato = random.choice(tipos_contrato)
                tratativa = random.choice(tratativas)
                status_tratativa = random.choice(status_tratativas)
                entregue_por = random.choice(entregue_por_options)
                
                # Gerar IDs de equipamentos únicos
                equipamentos_ids = []
                for j in range(random.randint(1, 5)):
                    equipamentos_ids.append(f"ID{i+1:03d}{j+1:02d}")
                
                # Gerar números de equipamentos
                numeros_equipamentos = []
                for j in range(random.randint(1, 3)):
                    numeros_equipamentos.append(f"EQ{i+1:04d}{j+1:02d}")
                
                # Criar manutenção
                manutencao = registrodemanutencao.objects.create(
                    nome=cliente,
                    tipo_entrada=tipo_entrada,
                    tipo_produto=produto,
                    motivo=motivo,
                    tipo_customizacao=customizacao,
                    recebimento='Recebido',
                    entregue_por_retirado_por=entregue_por,
                    id_equipamentos=', '.join(equipamentos_ids),
                    quantidade=len(equipamentos_ids),
                    tipo_contrato=tipo_contrato,
                    customizacaoo=customizacao,
                    numero_equipamento=', '.join(numeros_equipamentos),
                    observacoes=f"Registro de teste {i+1}. {motivo} identificado. {tratativa} em andamento. Cliente: {cliente.nome_fantasia}.",
                    tratativa=tratativa,
                    status=status,
                    status_tratativa=status_tratativa,
                    data_devolucao=timezone.now() + timedelta(days=random.randint(1, 30))
                )
                
                manutencoes_criadas.append(manutencao)
                self.stdout.write(f'✅ Registro {i+1} criado - ID: {manutencao.id} - Cliente: {cliente.nome_fantasia} - Status: {status}')
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao criar registro {i+1}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'🎉 {len(manutencoes_criadas)} registros criados com sucesso!'))
        
        # Mostrar estatísticas
        self.stdout.write('\n📈 Estatísticas dos Registros Criados:')
        
        total_manutencoes = registrodemanutencao.objects.count()
        self.stdout.write(f'📊 Total de manutenções no sistema: {total_manutencoes}')
        
        # Estatísticas por status
        self.stdout.write('\n📊 Distribuição por Status:')
        for status in status_options:
            count = registrodemanutencao.objects.filter(status=status).count()
            self.stdout.write(f'   {status}: {count}')
        
        # Estatísticas por tipo de entrada
        self.stdout.write('\n📊 Distribuição por Tipo de Entrada:')
        tipos = registrodemanutencao.objects.values_list('tipo_entrada', flat=True).distinct()
        for tipo in tipos:
            count = registrodemanutencao.objects.filter(tipo_entrada=tipo).count()
            self.stdout.write(f'   {tipo}: {count}')
        
        # Últimos registros criados
        self.stdout.write('\n🕒 Últimos 10 registros criados:')
        recentes = registrodemanutencao.objects.order_by('-data_criacao')[:10]
        for manutencao in recentes:
            self.stdout.write(f'   ID: {manutencao.id} - {manutencao.nome.nome_fantasia} - {manutencao.status} - {manutencao.data_criacao.strftime("%d/%m/%Y %H:%M")}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 REGISTROS CRIADOS COM SUCESSO!'))
        self.stdout.write('Agora você pode testar o sistema com dados reais!')
