from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CadastroTipoProduto(models.Model):
    """Modelo para cadastro de tipo de produto"""
    nome_produto = models.CharField(max_length=200, verbose_name="Nome do Produto")
    descricao = models.TextField(verbose_name="Descrição",null=True, blank=True)
    fabricante = models.CharField(max_length=200, verbose_name="Fabricante")
    telefone_fabricante = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email_fabricante = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Valor Unitário")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    
    class Meta:
        verbose_name = "Cadastro de Tipo de Produto"
        verbose_name_plural = "Cadastros de Tipos de Produtos"
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.nome_produto} - {self.fabricante}"
    
    def get_estoque_disponivel(self):
        """Calcula o estoque disponível para este tipo de produto"""
        try:
            # Calcula baseado nas movimentações de estoque
            movimentacoes = MovimentacaoEstoque.objects.filter(produto=self)
            
            total_entradas = 0
            total_saidas = 0
            
            for mov in movimentacoes:
                if mov.tipo == 'entrada':
                    total_entradas += mov.quantidade
                elif mov.tipo == 'saida':
                    total_saidas += mov.quantidade
            
            # Estoque disponível = entradas - saídas
            estoque_disponivel = total_entradas - total_saidas
            return max(0, estoque_disponivel)  # Não pode ser negativo
            
        except Exception as e:
            # Em caso de erro, retorna 0 para não bloquear o sistema
            print(f"Erro ao calcular estoque para produto {self.id}: {str(e)}")
            return 0
    
    def get_estoque_disponivel_legacy(self):
        """Método legado para calcular estoque baseado em entradas e requisições"""
        try:
            # Soma todas as entradas deste produto
            entradas = EntradaProduto.objects.filter(codigo_produto=self)
            total_entradas = sum(entrada.quantidade for entrada in entradas)
            
            # Soma todas as requisições pendentes/processadas deste produto
            # Import aqui para evitar import circular
            from django.apps import apps
            Requisicoes = apps.get_model('requisicoes', 'Requisicoes')
            requisicoes = Requisicoes.objects.filter(
                tipo_produto=self,
                status__in=['Pendente', 'Processando', 'Aprovado']
            )
            
            total_requisicoes = 0
            for req in requisicoes:
                try:
                    qtd = int(req.numero_de_equipamentos or 0)
                    total_requisicoes += qtd
                except (ValueError, TypeError):
                    # Se não conseguir converter, ignora esta requisição
                    continue
            
            # Estoque disponível = entradas - requisições
            estoque_disponivel = total_entradas - total_requisicoes
            return max(0, estoque_disponivel)  # Não pode ser negativo
            
        except Exception as e:
            # Em caso de erro, retorna 0 para não bloquear o sistema
            print(f"Erro ao calcular estoque para produto {self.id}: {str(e)}")
            return 0

class EntradaProduto(models.Model):
    """Modelo para entrada de produto"""
    codigo_produto = models.ForeignKey(CadastroTipoProduto, on_delete=models.CASCADE, verbose_name="Código do Produto (FK)")
    quantidade = models.PositiveIntegerField(verbose_name="Quantidade")
    id_equipamento = models.CharField(max_length=100, verbose_name="ID (Número do Equipamento)")
    ids_equipamentos = models.TextField(blank=True, null=True, verbose_name="IDs dos Equipamentos (separados por vírgula)")
    ids_equipamentos_timestamps = models.TextField(blank=True, null=True, verbose_name="Timestamps dos IDs (JSON)")
    data = models.DateTimeField(verbose_name="Data (datetime)")
    valor_nota = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor de Nota (Valor de Compra)")
    numero_nota_fiscal = models.CharField(max_length=50, verbose_name="Número de Nota Fiscal")
    data_entrada = models.DateTimeField(auto_now_add=True, verbose_name="Data de Entrada")
    
    class Meta:
        verbose_name = "Entrada de Produto"
        verbose_name_plural = "Entradas de Produtos"
        ordering = ['-data_entrada']
    
    def __str__(self):
        return f"{self.codigo_produto.nome_produto} - Qtd: {self.quantidade} - NF: {self.numero_nota_fiscal}"
    
    def get_ids_equipamentos_list(self):
        """Retorna lista dos IDs dos equipamentos"""
        if self.ids_equipamentos:
            return [id.strip() for id in self.ids_equipamentos.split(',') if id.strip()]
        return [self.id_equipamento] if self.id_equipamento else []
    
    def get_ids_equipamentos_timestamps(self):
        """Retorna dicionário com IDs e seus timestamps"""
        import json
        if self.ids_equipamentos_timestamps:
            try:
                return json.loads(self.ids_equipamentos_timestamps)
            except:
                return {}
        return {}
    
    def add_id_equipamento(self, novo_id):
        """Adiciona um novo ID de equipamento à lista com timestamp"""
        import json
        from django.utils import timezone
        
        ids_existentes = self.get_ids_equipamentos_list()
        timestamps = self.get_ids_equipamentos_timestamps()
        
        if novo_id not in ids_existentes:
            ids_existentes.append(novo_id)
            timestamps[novo_id] = timezone.now().isoformat()
            
            self.ids_equipamentos = ', '.join(ids_existentes)
            self.ids_equipamentos_timestamps = json.dumps(timestamps)
            self.save()
    
    def get_quantidade_ids(self):
        """Retorna a quantidade de IDs únicos de equipamentos"""
        return len(self.get_ids_equipamentos_list())
    
    def get_historico_ids(self):
        """Retorna histórico detalhado dos IDs com timestamps"""
        from django.utils import timezone
        from datetime import datetime
        
        timestamps = self.get_ids_equipamentos_timestamps()
        historico = []
        
        for id_equip in self.get_ids_equipamentos_list():
            timestamp = timestamps.get(id_equip, self.data_entrada.isoformat())
            try:
                # Tentar parsear o timestamp
                if 'T' in timestamp:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                else:
                    dt = self.data_entrada
                data_formatada = dt.strftime('%d/%m/%Y %H:%M')
            except:
                data_formatada = self.data_entrada.strftime('%d/%m/%Y %H:%M')
            
            historico.append({
                'id': id_equip,
                'timestamp': timestamp,
                'data_formatada': data_formatada
            })
        
        # Ordenar por timestamp
        historico.sort(key=lambda x: x['timestamp'])
        return historico
    
    def save(self, *args, **kwargs):
        """Override do save para registrar movimentação de estoque"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Registrar entrada de estoque
            MovimentacaoEstoque.objects.create(
                produto=self.codigo_produto,
                tipo='entrada',
                quantidade=self.quantidade,
                motivo=f'Entrada de produto - NF: {self.numero_nota_fiscal}',
                referencia=f'ENTRADA_{self.id}'
            )

class MovimentacaoEstoque(models.Model):
    """Modelo para rastrear movimentações de estoque"""
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
    ]
    
    produto = models.ForeignKey(CadastroTipoProduto, on_delete=models.CASCADE, verbose_name="Produto")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimentação")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    motivo = models.CharField(max_length=200, verbose_name="Motivo")
    referencia = models.CharField(max_length=100, blank=True, null=True, verbose_name="Referência (ID da Requisição, etc.)")
    data_movimentacao = models.DateTimeField(auto_now_add=True, verbose_name="Data da Movimentação")
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")
    
    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']
    
    def __str__(self):
        return f"{self.produto.nome_produto} - {self.get_tipo_display()} - {self.quantidade} - {self.motivo}"