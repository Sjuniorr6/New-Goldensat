from django.db import models
from clientes.models import Clientes   
from produtos.models import CadastroTipoProduto    
from django.utils import timezone
class Requisicoes(models.Model):
    # Definição das escolhas de status
    statuschoice = [
        ('Aprovado', 'Aprovado'),
        ('Reprovado', 'Reprovado'),
        ('Pendente', 'Pendente'),
        ('Configurado', 'Configurado'),
        ('Expedido', 'Expedido'),
    ]

    # Definição das escolhas de TP (tempo de processamento)
    TP = [
        ('5', '5'),
        ('10', '10'),
        ('15', '15'),
        ('30', '30'),
        ('60', '60'),
        ('360', '360'),
        ('720', '720'),
    ]
    statusfat = [
        ('Pendente', 'Pendente'),
        ('Faturado sem taxa', 'Faturado sem taxa'),
        ('Faturado com taxa', 'Faturado com taxa'),
        ('Pendente sem Contrato', 'Pendente sem Contrato'),
        ('Pendente Sem Termo', 'Pendente Sem Termo'),
        ('Sem Custo', 'Sem Custo'),
        ('Dados invalidos', 'Dados invalidos'),
        ('Reprovado Pelo CEO','Reprovado Pelo CEO'),
    ]
    motivoc = [
        ('Tipo de Faturamento', 'Tipo de Faturamento'),
        ('Aquisicão Nova', 'Aquisicão Nova'),
        ('Manutenção', 'Manutenção'),
        ('Aditivo', 'Aditivo'),
        ('Acessórios', 'Acessórios'),
        ('Extravio', 'Extravio'),
        ('Teste', 'Teste'),
        ('Spot','Spot'),
        ('Isca Fast', 'Isca Fast'),
        ('Isca Fast - Agente', 'Isca Fast - Agente'),
        ('Antenista', 'Antenista'),
        ('Reversa', 'Reversa'),
        ('Isca FAST', 'Isca FAST'),
        ('Estoque Antenista', 'Estoque Antenista'),
        ('Renovação', 'Renovação'),
    ]


    # Definição das escolhas de tipo de envio
    tipo_envio = [
        ('Agente', 'Agente'),
        ('Retirada na base', 'Retirada na base'),
        ('Motoboy', 'Motoboy'),
        ('transportadora', 'Transportadora'),
        ('Correio', 'Correio'),
        ('Comercial', 'Comercial'),
    ]

    # Definição das escolhas de tipo de contrato
    contrato_tipo = [
        ('', ''),
        ('Descartavel', 'Descartavel'),
        ('Retornavel', 'Retornavel'),
    ]

    # Definição das escolhas de tipo de fatura
    fatura_tipo = [
        ('Com Custo', 'Com Custo'),
        ('Sem Custo', 'Sem Custo'),
    ]

    # Definição das escolhas de status
    STATUS_CHOICES = [
        
        ('Pendente', 'Pendente'),
        ('Configurado', 'Configurado'),
        ('Reprovado pelo CEO', 'Reprovado pelo CEO'),
        ('Aprovado pelo CEO', 'Aprovado pelo CEO'),
        ('Enviado para o cliente', 'Enviado para o cliente'),
    ]
    customizacoes = [

        ('Sem custumização' , 'Sem custumização'),
        ('Caixa de papelão' , 'Caixa de papelão' ),
        ('Caixa de papelão (bateria desacoplada)' , 'Caixa de papelão (bateria desacoplada)'),
        ('Caixa de papelão + DF' , 'Caixa de papelão + DF'),
        ('Termo branco' , 'Termo branco'),
        ('Termo branco + imã' , 'Termo branco + imã'),
        ('Termo branco + D.F ' , 'Termo branco + D.F'),
        ('Termo branco slim ' , 'Termo branco slim'),
        ('Termo branco slim + D.F +EQT  ' , 'Termo branco slim + D.F +EQT'),
        ('Termo cinza slim + D.F +EQT  ' , 'Termo cinza slim + D.F +EQT'),
        ('Termo branco  (isopor) ' , 'Termo branco  (isopor)'),
        ('Termo branco - bateria externa ' , 'Termo branco - bateria externa'),
        ('Termo marrom + imã' , 'Termo marrom + imã'),
        ('Termo cinza' , 'Termo cinza'),
        ('Termo cinza + imã' , 'Termo cinza + imã'),
        ('Termo preto' , 'Termo preto'),
        ('Termo preto + imã' , 'Termo preto + imã'),
        ('Termo branco - slim' , 'Termo branco - slim'),
        ('Termo marrom slim +D.F + EQT' , 'Termo marrom slim +D.F + EQT'),
        ('Termo marrom' , 'Termo marrom'),
        ('Termo marrom + ETQ' , 'Termo marrom + ETQ'),
        ('Termo marrom slim' , 'Termo marrom slim'),
        ('Caixa blindada' , 'Caixa blindada'),
        ('Tênis/ Sapato' , 'Tênis/ Sapato'),
        ('Projetor' , 'Projetor'),
        ('Caixa de som' , 'Caixa de som'),
        ('Luminaria' , 'Luminaria'),
        ('Alexa' , 'Alexa'),
        ('Video Game' , 'Video Game'),
        ('Secador de cabelo' , 'Secador de cabelo'),
        ('Roteador' , 'Roteador'),
        ('Relogio digital' , 'Relogio digital'),


    ]
    meses = [
    ('N/A', 'N/A'),
    ('6', '6'),
    ('12', '12'),
    ('18', '18'),
    ('24', '24'),
    ('30', '30'),
    ('36', '36'),
    ('48', '48'),
]
    ANTENISTA_CHOICES = [
    ('RODRIGO SILVA', 'RODRIGO SILVA'),
    ('FELIPPE CAMELO', 'FELIPPE CAMELO'),
    ('FILIPPE CAMELO', 'FILIPPE CAMELO'),
    ('JOSÉ ANTONIO', 'JOSÉ ANTONIO'),
    ('CESAR RODRIGO - SPO', 'CESAR RODRIGO - SPO'),
    ('LUCIO', 'LUCIO'),
    ('FELIPE MACEDO - SPO', 'FELIPE MACEDO - SPO'),
    ('RAFAEL ALVES - SPO', 'RAFAEL ALVES - SPO'),
    ('ANDERSON COSTA / L', 'ANDERSON COSTA / L'),
    ('YURI NETTO', 'YURI NETTO'),
    ('HERCULES / FILIPE', 'HERCULES / FILIPE'),
    ('ALEXANDRE', 'ALEXANDRE'),
    ('AILTON', 'AILTON'),
    ('SATURNINO', 'SATURNINO'),
    ('CLEBSON ARANDU - SPO', 'CLEBSON ARANDU - SPO'),
    ('TENORIO', 'TENORIO'),
    ('WILSON JOSE', 'WILSON JOSE'),
    ('WESLEY RODRIGO', 'WESLEY RODRIGO'),
    ('WESLEY RODRIGO - SPO', 'WESLEY RODRIGO - SPO'),
    ('ANGELO/AGATHA', 'ANGELO/AGATHA'),
    ('STEVERSON ROGGER', 'STEVERSON ROGGER'),
    ('IGOR BARBOSA', 'IGOR BARBOSA'),
    ('CAIQUE GONÇALVES', 'CAIQUE GONÇALVES'),
    ('GIOVAN MENDES', 'GIOVAN MENDES'),
    ('RONALDO/SILVA', 'RONALDO/SILVA'),
    ('CARDOSO/PAULA', 'CARDOSO/PAULA'),
    ('BORGES / ALMEIDA - JONAS', 'BORGES / ALMEIDA - JONAS'),
    ('DINAYDER/CLEITON - JONAS', 'DINAYDER/CLEITON - JONAS'),
    ('IVAN/LEANDRO - ALEX', 'IVAN/LEANDRO - ALEX'),
    ('WILSON JOSE - SPO', 'WILSON JOSE - SPO'),
    ('VINICIUS SUHE', 'VINICIUS SUHE'),
    ('AURELIO ANDRADE - RJ', 'AURELIO ANDRADE - RJ'),
    ('THAISY/JOAO PEDRO', 'THAISY/JOAO PEDRO'),
    ('PAULO VICENTE/LUCIA - JONAS', 'PAULO VICENTE/LUCIA - JONAS'),
    ('ANDERSON NOGUEIRA', 'ANDERSON NOGUEIRA'),
    ('THIAGO MATHEUS - SPO', 'THIAGO MATHEUS - SPO'),
    ('SIMEI SANTANA - SPO', 'SIMEI SANTANA - SPO'),
    ('FLORIANO FERREIRA - SPO', 'FLORIANO FERREIRA - SPO'),
    ('AURELIO', 'AURELIO'),
    ('RAPHAEL/LIMA', 'RAPHAEL/LIMA'),
    ('RIBEIRO/DUTRA', 'RIBEIRO/DUTRA'),
    ('HUGO/MOTTA', 'HUGO/MOTTA'),
    ('ANDRADE/LEONARDO', 'ANDRADE/LEONARDO'),
    ('ANDERSON/MARCIO', 'ANDERSON/MARCIO'),
    ('SILVIO ROMERO', 'SILVIO ROMERO'),
    ('ALEX SILVA', 'ALEX SILVA'),
    ('GABRIEL QUILANTE', 'GABRIEL QUILANTE'),
    ('VITOR ROGERIO', 'VITOR ROGERIO'),
    ('MARCIO JUNIOR', 'MARCIO JUNIOR'),
    ('TADEU', 'TADEU'),
    ('LEANDRO FERREIRA - RJ', 'LEANDRO FERREIRA - RJ'),
    ('NASCIMENTO/AMERSON', 'NASCIMENTO/AMERSON'),
    ('IZABEL/SAMPAIO', 'IZABEL/SAMPAIO'),
    ('ANDRE/TELES', 'ANDRE/TELES'),
    ('ALLAN/CRISTINA', 'ALLAN/CRISTINA'),
    ('CARLOS MAIA/FELIPE SOUSA', 'CARLOS MAIA/FELIPE SOUSA'),
    ('FELIPE SOUZA', 'FELIPE SOUZA'),
    ('ROBSON RAMIRO', 'ROBSON RAMIRO'),
    ('WASHINGTON FERNANDES - RJ', 'WASHINGTON FERNANDES - RJ'),
    ('CARLOS CARVALHO/DIOGO SENA', 'CARLOS CARVALHO/DIOGO SENA'),
    ('ROGERIO/ISMAEL', 'ROGERIO/ISMAEL'),
    ('JANDERSO FERNANDES', 'JANDERSO FERNANDES'),
    ('JOAO MARCOS', 'JOAO MARCOS'),
    ('ADRIANO GONÇALVES', 'ADRIANO GONÇALVES'),
    ('COUTINHO/SANTOS', 'COUTINHO/SANTOS'),
    ('NUNES/CRYSOSTOMO', 'NUNES/CRYSOSTOMO'),
    ('ESTEVAO/ULYSSES', 'ESTEVAO/ULYSSES'),
    ('ALCIDES', 'ALCIDES'),
    ('EZEQUIEL', 'EZEQUIEL'),
    ('NILDO', 'NILDO'),
    ('ALEX', 'ALEX'),
    ('ANDERSON', 'ANDERSON'),
    ('ANTONIEQUE', 'ANTONIEQUE'),
    ('OSNI', 'OSNI'),
    ('ELTON', 'ELTON'),
    ('NEY', 'NEY'),
    ('ANDRÉ', 'ANDRÉ'),
    ('RILDO', 'RILDO'),
    ('WELLINGTHON', 'WELLINGTHON'),
    ('GERSON WALACE', 'GERSON WALACE'),
    ('JUSTINO', 'JUSTINO'),
    ('ANTONIO', 'ANTONIO'),
    ('FRANCISCO', 'FRANCISCO'),
    ('OSMAN', 'OSMAN'),
    ('TONHARA', 'TONHARA'),
    ('EMERSON', 'EMERSON'),
    ('MARCELO', 'MARCELO'),
    ('JEFFERSON', 'JEFFERSON'),
    ('GUILHERME', 'GUILHERME'),
    ('MARCIO', 'MARCIO'),
    ('SAMPAIO', 'SAMPAIO'),
    ('DIOGO', 'DIOGO'),
    ('WESLEY', 'WESLEY'),
    ('EVERALDO / SAMUEL', 'EVERALDO / SAMUEL'),
    ('ERIK', 'ERIK'),
    ('LUCAS CARVALHO', 'LUCAS CARVALHO'),
    ('RODRIGO', 'RODRIGO'),
    ('PITTA', 'PITTA'),
    ('JUSTO', 'JUSTO'),
    ('PAULO HENRIQUE', 'PAULO HENRIQUE'),
    ('EDUARDO', 'EDUARDO'),
    ('YURI', 'YURI'),
    ('RAFAEL', 'RAFAEL'),
    ('MARLON', 'MARLON'),
    ('MALLONE ROCHA DA SILVA', 'MALLONE ROCHA DA SILVA'),
    ('Ian Carlos Severino', 'Ian Carlos Severino'),
    ('Matheus (Praia Grande)', 'Matheus (Praia Grande)'),
    ('André Tsubamoto | Uniforme Seguros', 'André Tsubamoto | Uniforme Seguros'),
    ('Fernandes - Nordeste Seguros', 'Fernandes - Nordeste Seguros'),
    ('RAY ALBINO -MOGIGUAÇU/SP','RAY ALBINO -MOGIGUAÇU/SP'),
    ('Barbosa - Nordeste Seguros de FORTALEZA','Barbosa - Nordeste Seguros de FORTALEZA'),	
    ('Kelly - DeCaprio Seguros de Belo Horizonte','Kelly - DeCaprio Seguros de Belo Horizonte'),
    ('Gilmar Dutra - Natal / RN','Gilmar Dutra - Natal / RN'),
    ('Redvagner Schroeder Silva / Atibaia - SP', 'Redvagner Schroeder Silva / Atibaia - SP'),
    ('Marcio Raimundo da Silva / Pouso Alegre - MG', 'Marcio Raimundo da Silva / Pouso Alegre - MG'),
    ('osé Nilton Costa de Souza / Petrolina - PE', 'osé Nilton Costa de Souza / Petrolina - PE'),
    ('João Paulo Alexandre da Silva | Maceió - BA', 'João Paulo Alexandre da Silva | Maceió - BA'),
    ('Andrei Angelim Pinheiro - MANAUS - AM', 'Andrei Angelim Pinheiro - MANAUS - AM'),
    ('Valdeci Nunes Neto - Itajaí','Valdeci Nunes Neto - Itajaí'),
    ('Oscar Carneiro de Souza Junior','Oscar Carneiro de Souza Junior'),
]
    comercial_choices = [

        ('MAYRA','MAYRA'),
        ('DANIEL','DANIEL'),
        ('MARCIO','MARCIO'),
        ('CIDO','CIDO'),
        ('ALISON','ALISON'),
        ('THIAGO','THIAGO'),
        ('GOLDEN','GOLDEN'),
        ('ARMANDO','ARMANDO'),
        ('INFINITY','INFINITY')

    ]

    # Campos do modelo
    id = models.AutoField(primary_key=True)
    nome = models.ForeignKey(Clientes, on_delete=models.CASCADE, related_name='requisicoes_nome')
    endereco = models.CharField(max_length=255, blank=True, null=True)
    contrato = models.CharField(choices=contrato_tipo, null=True, blank=True, max_length=50)
    cnpj = models.CharField(max_length=25, blank=True, null=True)
    numero_de_equipamentos = models.CharField(max_length=14, blank=True, null=True)
    inicio_de_contrato = models.DateField(blank=True, null=True)
    vigencia = models.CharField(max_length=50,choices=meses,blank=True, null=True)
    customizacao = models.CharField(max_length=50,choices=meses,blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(default=timezone.now)
    data_entrega = models.DateField(blank=True, null=True)
    tipo_customizacao = models.CharField(choices=customizacoes ,null=True,blank=True, max_length=50)
    antenista = models.CharField(choices= ANTENISTA_CHOICES,max_length=50, blank=True, null=True)  # Novo campo para antenistas
    envio = models.CharField(choices=tipo_envio, null=True, blank=True, max_length=50)
    taxa_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    comercial = models.CharField(choices=comercial_choices ,max_length=100, blank=True, default='')
    tipo_produto = models.ForeignKey(CadastroTipoProduto, on_delete=models.CASCADE, related_name='requisicoes_produto')
    carregador = models.CharField(max_length=100, blank=True, default='')
    motivo = models.CharField(choices=motivoc,  default='', null=True, blank=True, max_length=50)
    cabo = models.CharField(max_length=100, blank=True, default='')
    tipo_fatura = models.CharField(choices=fatura_tipo, null=True, blank=True, max_length=50)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    forma_pagamento = models.CharField(max_length=100,null=True, blank=True, default='')
    observacoes = models.TextField(max_length=250,null=True, blank=True, default='')
    aos_cuidados = models.TextField(max_length=250,null=True, blank=True, default='')
    status = models.CharField(choices=STATUS_CHOICES,default='Pendente', null=True, blank=True, max_length=50)
    TP = models.CharField(choices=TP, null=True, blank=True, max_length=50)
    status_faturamento = models.CharField(choices=statusfat,  default="Pendente",null=True, blank=True, max_length=50)
    id_equipamentos= models.TextField(max_length=180000, null=True, blank=True, default='')
    faturamento= models.CharField(choices=statusfat ,max_length=1200, blank=True, default='Pendente')
    iccid = models.CharField(max_length=600000,null=True, blank=True, default='')
    def __str__(self):
        return f"Requisição {self.id} - {self.nome} "






class estoque_antenista(models.Model):
    ANTENISTA_CHOICES =[
    ('RODRIGO SILVA', 'RODRIGO SILVA'),
    ('FELIPPE CAMELO', 'FELIPPE CAMELO'),
    ('FILIPPE CAMELO', 'FILIPPE CAMELO'),
    ('JOSÉ ANTONIO', 'JOSÉ ANTONIO'),
    ('CESAR RODRIGO - SPO', 'CESAR RODRIGO - SPO'),
    ('LUCIO', 'LUCIO'),
    ('FELIPE MACEDO - SPO', 'FELIPE MACEDO - SPO'),
    ('RAFAEL ALVES - SPO', 'RAFAEL ALVES - SPO'),
    ('ANDERSON COSTA / L', 'ANDERSON COSTA / L'),
    ('YURI NETTO', 'YURI NETTO'),
    ('HERCULES / FILIPE', 'HERCULES / FILIPE'),
    ('ALEXANDRE', 'ALEXANDRE'),
    ('AILTON', 'AILTON'),
    ('SATURNINO', 'SATURNINO'),
    ('CLEBSON ARANDU - SPO', 'CLEBSON ARANDU - SPO'),
    ('TENORIO', 'TENORIO'),
    ('WILSON JOSE', 'WILSON JOSE'),
    ('WESLEY RODRIGO', 'WESLEY RODRIGO'),
    ('WESLEY RODRIGO - SPO', 'WESLEY RODRIGO - SPO'),
    ('ANGELO/AGATHA', 'ANGELO/AGATHA'),
    ('STEVERSON ROGGER', 'STEVERSON ROGGER'),
    ('IGOR BARBOSA', 'IGOR BARBOSA'),
    ('CAIQUE GONÇALVES', 'CAIQUE GONÇALVES'),
    ('GIOVAN MENDES', 'GIOVAN MENDES'),
    ('RONALDO/SILVA', 'RONALDO/SILVA'),
    ('CARDOSO/PAULA', 'CARDOSO/PAULA'),
    ('BORGES / ALMEIDA - JONAS', 'BORGES / ALMEIDA - JONAS'),
    ('DINAYDER/CLEITON - JONAS', 'DINAYDER/CLEITON - JONAS'),
    ('IVAN/LEANDRO - ALEX', 'IVAN/LEANDRO - ALEX'),
    ('WILSON JOSE - SPO', 'WILSON JOSE - SPO'),
    ('VINICIUS SUHE', 'VINICIUS SUHE'),
    ('AURELIO ANDRADE - RJ', 'AURELIO ANDRADE - RJ'),
    ('THAISY/JOAO PEDRO', 'THAISY/JOAO PEDRO'),
    ('PAULO VICENTE/LUCIA - JONAS', 'PAULO VICENTE/LUCIA - JONAS'),
    ('ANDERSON NOGUEIRA', 'ANDERSON NOGUEIRA'),
    ('THIAGO MATHEUS - SPO', 'THIAGO MATHEUS - SPO'),
    ('SIMEI SANTANA - SPO', 'SIMEI SANTANA - SPO'),
    ('FLORIANO FERREIRA - SPO', 'FLORIANO FERREIRA - SPO'),
    ('AURELIO', 'AURELIO'),
    ('RAPHAEL/LIMA', 'RAPHAEL/LIMA'),
    ('RIBEIRO/DUTRA', 'RIBEIRO/DUTRA'),
    ('HUGO/MOTTA', 'HUGO/MOTTA'),
    ('ANDRADE/LEONARDO', 'ANDRADE/LEONARDO'),
    ('ANDERSON/MARCIO', 'ANDERSON/MARCIO'),
    ('SILVIO ROMERO', 'SILVIO ROMERO'),
    ('ALEX SILVA', 'ALEX SILVA'),
    ('GABRIEL QUILANTE', 'GABRIEL QUILANTE'),
    ('VITOR ROGERIO', 'VITOR ROGERIO'),
    ('MARCIO JUNIOR', 'MARCIO JUNIOR'),
    ('TADEU', 'TADEU'),
    ('LEANDRO FERREIRA - RJ', 'LEANDRO FERREIRA - RJ'),
    ('NASCIMENTO/AMERSON', 'NASCIMENTO/AMERSON'),
    ('IZABEL/SAMPAIO', 'IZABEL/SAMPAIO'),
    ('ANDRE/TELES', 'ANDRE/TELES'),
    ('ALLAN/CRISTINA', 'ALLAN/CRISTINA'),
    ('CARLOS MAIA/FELIPE SOUSA', 'CARLOS MAIA/FELIPE SOUSA'),
    ('FELIPE SOUZA', 'FELIPE SOUZA'),
    ('ROBSON RAMIRO', 'ROBSON RAMIRO'),
    ('WASHINGTON FERNANDES - RJ', 'WASHINGTON FERNANDES - RJ'),
    ('CARLOS CARVALHO/DIOGO SENA', 'CARLOS CARVALHO/DIOGO SENA'),
    ('ROGERIO/ISMAEL', 'ROGERIO/ISMAEL'),
    ('JANDERSO FERNANDES', 'JANDERSO FERNANDES'),
    ('JOAO MARCOS', 'JOAO MARCOS'),
    ('ADRIANO GONÇALVES', 'ADRIANO GONÇALVES'),
    ('COUTINHO/SANTOS', 'COUTINHO/SANTOS'),
    ('NUNES/CRYSOSTOMO', 'NUNES/CRYSOSTOMO'),
    ('ESTEVAO/ULYSSES', 'ESTEVAO/ULYSSES'),
    ('ALCIDES', 'ALCIDES'),
    ('EZEQUIEL', 'EZEQUIEL'),
    ('NILDO', 'NILDO'),
    ('ALEX', 'ALEX'),
    ('ANDERSON', 'ANDERSON'),
    ('ANTONIEQUE', 'ANTONIEQUE'),
    ('OSNI', 'OSNI'),
    ('ELTON', 'ELTON'),
    ('NEY', 'NEY'),
    ('ANDRÉ', 'ANDRÉ'),
    ('RILDO', 'RILDO'),
    ('WELLINGTHON', 'WELLINGTHON'),
    ('GERSON WALACE', 'GERSON WALACE'),
    ('JUSTINO', 'JUSTINO'),
    ('ANTONIO', 'ANTONIO'),
    ('FRANCISCO', 'FRANCISCO'),
    ('OSMAN', 'OSMAN'),
    ('TONHARA', 'TONHARA'),
    ('EMERSON', 'EMERSON'),
    ('MARCELO', 'MARCELO'),
    ('JEFFERSON', 'JEFFERSON'),
    ('GUILHERME', 'GUILHERME'),
    ('MARCIO', 'MARCIO'),
    ('SAMPAIO', 'SAMPAIO'),
    ('DIOGO', 'DIOGO'),
    ('WESLEY', 'WESLEY'),
    ('EVERALDO / SAMUEL', 'EVERALDO / SAMUEL'),
    ('ERIK', 'ERIK'),
    ('LUCAS CARVALHO', 'LUCAS CARVALHO'),
    ('RODRIGO', 'RODRIGO'),
    ('PITTA', 'PITTA'),
    ('JUSTO', 'JUSTO'),
    ('PAULO HENRIQUE', 'PAULO HENRIQUE'),
    ('EDUARDO', 'EDUARDO'),
    ('YURI', 'YURI'),
    ('RAFAEL', 'RAFAEL'),
    ('MARLON', 'MARLON'),
    ('MALLONE ROCHA DA SILVA', 'MALLONE ROCHA DA SILVA'),
    ('Ian Carlos Severino', 'Ian Carlos Severino'), 
    ('RAY ALBINO -MOGIGUAÇU/SP','RAY ALBINO -MOGIGUAÇU/SP'),
   ('Barbosa - Nordeste Seguros de FORTALEZA','Barbosa - Nordeste Seguros de FORTALEZA'),
   ('Kelly - DeCaprio Seguros de Belo Horizonte','Kelly - DeCaprio Seguros de Belo Horizonte'),
   ('Gilmar Dutra - Natal / RN','Gilmar Dutra - Natal / RN'),
    ('Redvagner Schroeder Silva / Atibaia - SP', 'Redvagner Schroeder Silva / Atibaia - SP'),
    ('Marcio Raimundo da Silva / Pouso Alegre - MG', 'Marcio Raimundo da Silva / Pouso Alegre - MG'),
    ('osé Nilton Costa de Souza / Petrolina - PE', 'osé Nilton Costa de Souza / Petrolina - PE'),
    ('João Paulo Alexandre da Silva | Maceió - BA', 'João Paulo Alexandre da Silva | Maceió - BA'),
    ('Andrei Angelim Pinheiro - MANAUS - AM', 'Andrei Angelim Pinheiro - MANAUS - AM'),
    ('Valdeci Nunes Neto - Itajaí','Valdeci Nunes Neto - Itajaí'),
    ('Oscar Carneiro de Souza Junior','Oscar Carneiro de Souza Junior'),
]

    nome = models.CharField(max_length=50, choices=ANTENISTA_CHOICES)
    tipo_produto = models.ForeignKey(CadastroTipoProduto, on_delete=models.CASCADE, related_name='antenista_produto')
    endereco = models.CharField(max_length=255, blank=True, null=True)
    quantidade = models.IntegerField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.nome} - {self.tipo_produto}"

    def save(self, *args, **kwargs):
        print(f"Salvando estoque: {self.nome} - {self.tipo_produto} com quantidade: {self.quantidade}")
        super().save(*args, **kwargs)



from django.contrib.auth.models import User
from django.db import models

class ControleModel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cliente = models.CharField(max_length=50, null=True, blank=True)
    requisicao_id = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento1 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento1 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento2 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento2 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento3 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento3 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento4 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento4 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento5 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento5 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento6 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento6 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento7 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento7 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento8 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento8 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento9 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento9 = models.CharField(max_length=50, null=True, blank=True)
    iccid_equipamento10 = models.CharField(max_length=50, null=True, blank=True)
    id_equipamento10 = models.CharField(max_length=50, null=True, blank=True)
    data = models.DateField(auto_now_add=True, null=True)
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Controle {self.id} - Cliente {self.cliente}"




from .models import estoque_antenista

class antenista_CARD(models.Model):
    ANTENISTA_CHOICES =[
('RODRIGO SILVA', 'RODRIGO SILVA'),
('FELIPPE CAMELO', 'FELIPPE CAMELO'),
('FILIPPE CAMELO', 'FILIPPE CAMELO'),
('JOSÉ ANTONIO', 'JOSÉ ANTONIO'),
('CESAR RODRIGO - SPO', 'CESAR RODRIGO - SPO'),
('LUCIO', 'LUCIO'),
('FELIPE MACEDO - SPO', 'FELIPE MACEDO - SPO'),
('RAFAEL ALVES - SPO', 'RAFAEL ALVES - SPO'),
('ANDERSON COSTA / L', 'ANDERSON COSTA / L'),
('YURI NETTO', 'YURI NETTO'),
('HERCULES / FILIPE', 'HERCULES / FILIPE'),
('ALEXANDRE', 'ALEXANDRE'),
('AILTON - CURITIBA /PR', 'AILTON - CURITIBA /PR'),
('SATURNINO', 'SATURNINO'),
('CLEBSON ARANDU - SPO', 'CLEBSON ARANDU - SPO'),
('TENORIO', 'TENORIO'),
('WILSON JOSE', 'WILSON JOSE'),
('WESLEY RODRIGO', 'WESLEY RODRIGO'),
('WESLEY RODRIGO - SPO', 'WESLEY RODRIGO - SPO'),
('ANGELO/AGATHA', 'ANGELO/AGATHA'),
('STEVERSON ROGGER', 'STEVERSON ROGGER'),
('IGOR BARBOSA', 'IGOR BARBOSA'),
('CAIQUE GONÇALVES', 'CAIQUE GONÇALVES'),
('GIOVAN MENDES', 'GIOVAN MENDES'),
('RONALDO/SILVA', 'RONALDO/SILVA'),
('CARDOSO/PAULA', 'CARDOSO/PAULA'),
('BORGES / ALMEIDA - JONAS', 'BORGES / ALMEIDA - JONAS'),
('DINAYDER/CLEITON - JONAS', 'DINAYDER/CLEITON - JONAS'),
('IVAN/LEANDRO - ALEX', 'IVAN/LEANDRO - ALEX'),
('WILSON JOSE - SPO', 'WILSON JOSE - SPO'),
('VINICIUS SUHE', 'VINICIUS SUHE'),
('AURELIO ANDRADE - RJ', 'AURELIO ANDRADE - RJ'),
('THAISY/JOAO PEDRO', 'THAISY/JOAO PEDRO'),
('PAULO VICENTE/LUCIA - JONAS', 'PAULO VICENTE/LUCIA - JONAS'),
('ANDERSON NOGUEIRA', 'ANDERSON NOGUEIRA'),
('THIAGO MATHEUS - SPO', 'THIAGO MATHEUS - SPO'),
('SIMEI SANTANA - SPO', 'SIMEI SANTANA - SPO'),
('FLORIANO FERREIRA - SPO', 'FLORIANO FERREIRA - SPO'),
('AURELIO', 'AURELIO'),
('RAPHAEL/LIMA', 'RAPHAEL/LIMA'),
('RIBEIRO/DUTRA', 'RIBEIRO/DUTRA'),
('HUGO/MOTTA', 'HUGO/MOTTA'),
('ANDRADE/LEONARDO', 'ANDRADE/LEONARDO'),
('ANDERSON/MARCIO', 'ANDERSON/MARCIO'),
('SILVIO ROMERO', 'SILVIO ROMERO'),
('ALEX SILVA', 'ALEX SILVA'),
('GABRIEL QUILANTE', 'GABRIEL QUILANTE'),
('VITOR ROGERIO', 'VITOR ROGERIO'),
('MARCIO JUNIOR', 'MARCIO JUNIOR'),
('TADEU', 'TADEU'),
('LEANDRO FERREIRA - RJ', 'LEANDRO FERREIRA - RJ'),
('NASCIMENTO/AMERSON', 'NASCIMENTO/AMERSON'),
('IZABEL/SAMPAIO', 'IZABEL/SAMPAIO'),
('ANDRE/TELES', 'ANDRE/TELES'),
('ALLAN/CRISTINA', 'ALLAN/CRISTINA'),
('CARLOS MAIA/FELIPE SOUSA', 'CARLOS MAIA/FELIPE SOUSA'),
('FELIPE SOUZA', 'FELIPE SOUZA'),
('ROBSON RAMIRO', 'ROBSON RAMIRO'),
('WASHINGTON FERNANDES - RJ', 'WASHINGTON FERNANDES - RJ'),
('CARLOS CARVALHO/DIOGO SENA', 'CARLOS CARVALHO/DIOGO SENA'),
('ROGERIO/ISMAEL', 'ROGERIO/ISMAEL'),
('JANDERSO FERNANDES', 'JANDERSO FERNANDES'),
('JOAO MARCOS', 'JOAO MARCOS'),
('COUTINHO/SANTOS', 'COUTINHO/SANTOS'),
('NUNES/CRYSOSTOMO', 'NUNES/CRYSOSTOMO'),
('ESTEVAO/ULYSSES', 'ESTEVAO/ULYSSES'),
('ALCIDES - RIBEIRÃO PRETO/SP', 'ALCIDES - RIBEIRÃO PRETO/SP'),
('EZEQUIEL - GARANHUNS/PE', 'EZEQUIEL - GARANHUNS/PE'),
('NILDO LOPES - APARECIDA DE GOIANIA/GO', 'NILDO LOPES - APARECIDA DE GOIANIA/GO'),
('ALEX - ITAJAI/SC', 'ALEX - ITAJAI/SC'),
('ANDERSON', 'ANDERSON'),
('ANTONIEQUE - SALVADOR/BA', 'ANTONIEQUE - SALVADOR/BA'),
('OSNI', 'OSNI'),
('ELTON - GUARULHOS/SP', 'ELTON - GUARULHOS/SP'),
('NEY', 'NEY'),
('ANDRÉ', 'ANDRÉ'),
('RILDO', 'RILDO'),
('WELLINGTHON - TUCURUI/PA', 'WELLINGTHON - TUCURUI/PA'),
('GERSON WALACE - PARAGOMINAS/PA', 'GERSON WALACE - PARAGOMINAS/PA'),
('JUSTINO', 'JUSTINO'),
('ANTONIO - TERESINA/PI', 'ANTONIO - TERESINA/PI'),
('FRANCISCO', 'FRANCISCO'),
('OSMAN', 'OSMAN'),
('TONHARA', 'TONHARA'),
('EMERSON', 'EMERSON'),
('MARCELO', 'MARCELO'),
('JEFFERSON', 'JEFFERSON'),
('GUILHERME', 'GUILHERME'),
('MARCIO MENEZES - CONTAGEM/MG', 'MARCIO MENEZES - CONTAGEM/MG'),
('SAMPAIO - SERRA/ES', 'SAMPAIO - SERRA/ES'),
('DIOGO - SANTA ADELIA/SP', 'DIOGO - SANTA ADELIA/SP'),
('WESLEY - VARGINHA/MG', 'WESLEY - VARGINHA/MG'),
('EVERALDO / SAMUEL', 'EVERALDO / SAMUEL'),
('ERIK', 'ERIK'),
('LUCAS CARVALHO', 'LUCAS CARVALHO'),
('RODRIGO', 'RODRIGO'),
('PITTA', 'PITTA'),
('JUSTO', 'JUSTO'),
('PAULO HENRIQUE', 'PAULO HENRIQUE'),
('EDUARDO - CAXIAS DO SUL/RS', 'EDUARDO - CAXIAS DO SUL/RS'),
('YURI BATALHA - VIAMÃO/RS', 'YURI BATALHA - VIAMÃO/RS'),
('RAFAEL BERTOLLO - SANTA MARIA/RS', 'RAFAEL BERTOLLO - SANTA MARIA/RS'),
('MARLON', 'MARLON'),
('MALLONE ROCHA DA SILVA', 'MALLONE ROCHA DA SILVA'),
('Ian Carlos Severino', 'Ian Carlos Severino'),
('Matheus (Praia Grande)', 'Matheus (Praia Grande)'),
('André Tsubamoto | Uniforme Seguros', 'André Tsubamoto | Uniforme Seguros'),
('Fernandes - Nordeste Seguros', 'Fernandes - Nordeste Seguros'),
('Nordeste Seguros - Filial Recife', 'Nordeste Seguros - Filial Recife'),
('ALEX VIANA CAMPINAS /SP', 'ALEX VIANA - CAMPINAS /SP'),
('ANDREI MANAUS/AM', 'ANDREI MANAUS/AM'),
('ERIK- CAMPO DOS GOYTACAZES /RJ ','ERIK- CAMPO DOS GOYTACAZES /RJ '),
('SAMUEL - JUIZ DE FORA/MG', 'SAMUEL - JUIZ DE FORA/MG'), 
('JOÃO PAULO - MACEIO/AL', 'JOÃO PAULO - MACEIO/AL'),
('JOSÉ NILTON - PETROLINA/PE', 'JOSÉ NILTON - PETROLINA/PE'),
('JOSINEY - FEIRA DE SANTANA/BA', 'JOSINEY - FEIRA DE SANTANA/BA'),
('REDVAGNER -  ATIBAIA/SP', 'REDVAGNER -  ATIBAIA/SP'),
('RILDO LENNO -BELEM/PA', 'RILDO LENNO -BELEM/PA'),
('RODRIGO APARECIDO - JUNDIAI/SP', 'RODRIGO APARECIDO - JUNDIAI/SP'),
('CLEITON SILVA  - POÇOES/BA', 'CLEITON SILVA  - POÇOES/BA'),

]
    TIPO = [
     ('Retornavel','Retornavel'),
     ('Descartavel','Descartavel'),

     
 ]

    nome = models.CharField(max_length=50,choices=ANTENISTA_CHOICES, null=True, blank=True)
    tipo_produto = models.ForeignKey(CadastroTipoProduto, on_delete=models.CASCADE, related_name='antenista_card_produto')
    solicitante  = models.CharField(max_length=1000, blank=True, null=True)
    telefone = models.CharField(max_length=255, blank=True, null=True)
    cliente = models.CharField(max_length=1000, blank=True, null=True)
    quantidade = models.IntegerField(null=True, blank=True)
    equipamentos = models.CharField(max_length=1000, blank=True, null=True)
    contrato = models.CharField(choices=TIPO,max_length=1000, blank=True, null=True)
    valor_entrega  = models.CharField(max_length=1000, blank=True, null=True)
    data_criacao = models.DateField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Atualizado', 'Atualizado'),
            ('Reprovado', 'Reprovado'),
            ('Pendente', 'Pendente'),
            # Adicione outros status conforme necessário
        ],
        default='Pendente',
    )

    def __str__(self):
        return f"{self.nome} - {self.tipo_produto}"
