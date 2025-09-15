from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tickets.models import TicketModel

class Command(BaseCommand):
    help = 'Cria tickets de exemplo para testar o sistema'

    def handle(self, *args, **options):
        # Verificar se já existem tickets
        if TicketModel.objects.exists():
            self.stdout.write(
                self.style.WARNING('Já existem tickets no sistema. Pulando criação de exemplos.')
            )
            return

        # Buscar ou criar usuário de exemplo
        user, created = User.objects.get_or_create(
            username='usuario_teste',
            defaults={
                'email': 'teste@example.com',
                'first_name': 'Usuário',
                'last_name': 'Teste',
                'is_staff': False
            }
        )

        # Tickets de exemplo
        tickets_exemplo = [
            {
                'titulo': 'Erro ao salvar requisição',
                'descricao_erro': 'Ao tentar salvar uma nova requisição, o sistema apresenta erro 500. O erro ocorre especificamente quando seleciono o produto "TESTE - WERE IS MY CARGO" e preencho a quantidade de equipamentos.',
                'setor': 'Configuração',
                'prioridade': 'Alta',
                'status': 'Pendente'
            },
            {
                'titulo': 'Problema com validação de estoque',
                'descricao_erro': 'O sistema não está validando corretamente o estoque disponível. É possível criar requisições mesmo quando não há estoque suficiente.',
                'setor': 'Área Técnica',
                'prioridade': 'Crítica',
                'status': 'Em Andamento'
            },
            {
                'titulo': 'Relatório de tickets não está funcionando',
                'descricao_erro': 'Ao tentar gerar o relatório de tickets por período, o sistema retorna uma página em branco. Testei com diferentes períodos e o problema persiste.',
                'setor': 'Inteligência',
                'prioridade': 'Média',
                'status': 'Pendente'
            },
            {
                'titulo': 'Interface lenta no mobile',
                'descricao_erro': 'A interface do sistema está muito lenta quando acessada pelo celular. Especificamente na página de listagem de requisições, demora mais de 10 segundos para carregar.',
                'setor': 'Área Técnica',
                'prioridade': 'Média',
                'status': 'Resolvido'
            },
            {
                'titulo': 'Falta campo de observações',
                'descricao_erro': 'No formulário de criação de requisições, seria útil ter um campo de observações adicionais para incluir informações extras sobre a solicitação.',
                'setor': 'Comercial',
                'prioridade': 'Baixa',
                'status': 'Pendente'
            }
        ]

        # Criar tickets
        for i, ticket_data in enumerate(tickets_exemplo, 1):
            ticket = TicketModel.objects.create(
                usuario=user,
                titulo=ticket_data['titulo'],
                descricao_erro=ticket_data['descricao_erro'],
                setor=ticket_data['setor'],
                prioridade=ticket_data['prioridade'],
                status=ticket_data['status']
            )
            
            # Adicionar correção e devolutiva para tickets resolvidos
            if ticket.status == 'Resolvido':
                ticket.correcao = 'Otimizamos as consultas ao banco de dados e implementamos cache para melhorar a performance em dispositivos móveis.'
                ticket.devolutiva = 'Problema resolvido! A interface agora está mais rápida em dispositivos móveis. Teste e nos informe se ainda há algum problema.'
                ticket.save()

            self.stdout.write(
                self.style.SUCCESS(f'Ticket #{ticket.id} criado: {ticket.titulo}')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ {len(tickets_exemplo)} tickets de exemplo criados com sucesso!')
        )
        self.stdout.write(
            self.style.SUCCESS('🎫 Acesse o sistema de tickets para visualizar os exemplos.')
        )
