/**
 * CLIENTES.JS - Golden SAT
 * Sistema de gerenciamento de clientes
 */

console.log('🚀 CLIENTES.JS carregado!');

class ClientesManager {
    constructor() {
        this.init();
    }

    init() {
        console.log('🔧 Inicializando ClientesManager...');
        this.setupEventListeners();
        this.setupModals();
        this.setupFilters();
        console.log('✅ ClientesManager inicializado com sucesso!');
    }

    setupEventListeners() {
        console.log('🔧 Configurando event listeners...');
        
        // Formulário de cadastro
        const formCadastrar = document.getElementById('formCadastrarCliente');
        if (formCadastrar && !formCadastrar.hasAttribute('data-listener-added')) {
            formCadastrar.addEventListener('submit', (e) => this.handleCadastrarCliente(e));
            formCadastrar.setAttribute('data-listener-added', 'true');
            console.log('✅ Event listener do formulário de cadastro adicionado');
        }

        // Formulário de edição
        const formEditar = document.getElementById('formEditarCliente');
        if (formEditar && !formEditar.hasAttribute('data-listener-added')) {
            formEditar.addEventListener('submit', (e) => this.handleEditarCliente(e));
            formEditar.setAttribute('data-listener-added', 'true');
            console.log('✅ Event listener do formulário de edição adicionado');
        }

        // Botões de ação da tabela (usar event delegation para evitar duplicação)
        if (!this.tableActionListenerAdded) {
            document.addEventListener('click', (e) => {
                if (e.target.closest('.btn-action')) {
                    const button = e.target.closest('.btn-action');
                    const action = button.dataset.action;
                    const id = button.dataset.id;
                    this.handleTableAction(action, id);
                }
            });
            this.tableActionListenerAdded = true;
            console.log('✅ Event listener dos botões de ação adicionado');
        }

        // Confirmação de exclusão
        const btnConfirmarExclusao = document.getElementById('confirmarExclusaoCliente');
        if (btnConfirmarExclusao && !btnConfirmarExclusao.hasAttribute('data-listener-added')) {
            btnConfirmarExclusao.addEventListener('click', () => this.executarExclusaoCliente());
            btnConfirmarExclusao.setAttribute('data-listener-added', 'true');
            console.log('✅ Event listener do botão de exclusão adicionado');
        }
        
        console.log('✅ Event listeners configurados com sucesso!');
    }

    setupModals() {
        // Limpar formulários quando modais são fechados
        const modals = ['cadastrarClienteModal', 'editarClienteModal', 'excluirClienteModal'];
        modals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.addEventListener('hidden.bs.modal', () => {
                    this.limparFormularios(modalId);
                });
            }
        });
    }

    setupFilters() {
        // Filtros em tempo real
        const filtros = ['filtroNome', 'filtroCnpj', 'filtroStatus'];
        filtros.forEach(filtroId => {
            const elemento = document.getElementById(filtroId);
            if (elemento) {
                elemento.addEventListener('input', () => this.aplicarFiltros());
            }
        });
    }

    async handleCadastrarCliente(event) {
        event.preventDefault();
        console.log('Cadastrando cliente...');

        const form = event.target;
        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch('/clientes/cadastrar/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });

            const data = await response.json();
            console.log('Resposta do servidor:', data);

            if (data.success) {
                this.showSuccess('Cliente cadastrado com sucesso!');
                this.fecharModal('cadastrarClienteModal');
                // Atualizar tabela dinamicamente
                setTimeout(() => {
                    this.atualizarTabela();
                }, 1000);
            } else {
                this.showError(data.message || 'Erro ao cadastrar cliente');
                this.mostrarErrosFormulario(data.errors);
            }
        } catch (error) {
            console.error('Erro ao cadastrar cliente:', error);
            this.showError('Erro de conexão. Tente novamente.');
        }
    }

    async handleEditarCliente(event) {
        event.preventDefault();
        console.log('Editando cliente...');

        const form = event.target;
        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const clienteId = document.getElementById('cliente_id_edit').value;

        try {
            const response = await fetch(`/clientes/update/${clienteId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });

            const data = await response.json();
            console.log('Resposta do servidor:', data);

            if (data.success) {
                this.showSuccess('Cliente atualizado com sucesso!');
                this.fecharModal('editarClienteModal');
                // Atualizar tabela dinamicamente
                setTimeout(() => {
                    this.atualizarTabela();
                }, 1000);
            } else {
                this.showError(data.message || 'Erro ao atualizar cliente');
                this.mostrarErrosFormulario(data.errors);
            }
        } catch (error) {
            console.error('Erro ao editar cliente:', error);
            this.showError('Erro de conexão. Tente novamente.');
        }
    }

    handleTableAction(action, id) {
        console.log(`Ação: ${action}, ID: ${id}`);

        switch (action) {
            case 'visualizar':
                this.visualizarCliente(id);
                break;
            case 'editar':
                this.editarCliente(id);
                break;
            case 'excluir':
                this.excluirCliente(id);
                break;
            default:
                console.log('Ação não reconhecida:', action);
        }
    }

    async visualizarCliente(id) {
        console.log('Visualizando cliente ID:', id);

        try {
            const response = await fetch(`/clientes/detail/${id}/`);
            const data = await response.json();

            if (response.ok) {
                this.preencherModalDetalhes(data);
                this.abrirModal('visualizarClienteModal');
            } else {
                this.showError('Erro ao carregar detalhes do cliente');
            }
        } catch (error) {
            console.error('Erro ao visualizar cliente:', error);
            this.showError('Erro de conexão. Tente novamente.');
        }
    }

    async editarCliente(id) {
        console.log('Editando cliente ID:', id);

        try {
            const response = await fetch(`/clientes/detail/${id}/`);
            const data = await response.json();

            if (response.ok) {
                this.preencherFormularioEdicao(data);
                this.abrirModal('editarClienteModal');
            } else {
                this.showError('Erro ao carregar dados do cliente');
            }
        } catch (error) {
            console.error('Erro ao editar cliente:', error);
            this.showError('Erro de conexão. Tente novamente.');
        }
    }

    excluirCliente(id) {
        console.log('Excluindo cliente ID:', id);

        // Armazenar ID para exclusão
        this.clienteIdParaExclusao = id;

        // Buscar informações do cliente para mostrar no modal
        this.buscarInfoClienteParaExclusao(id);

        this.abrirModal('excluirClienteModal');
    }

    async buscarInfoClienteParaExclusao(id) {
        try {
            const response = await fetch(`/clientes/detail/${id}/`);
            const data = await response.json();

            if (response.ok) {
                const infoDiv = document.getElementById('infoClienteExclusao');
                infoDiv.innerHTML = `
                    <div class="alert alert-info">
                        <strong>Cliente:</strong> ${data.nome}<br>
                        <strong>CNPJ:</strong> ${data.cnpj}<br>
                        <strong>Status:</strong> ${data.status || 'N/A'}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Erro ao buscar informações do cliente:', error);
        }
    }

    async executarExclusaoCliente() {
        if (!this.clienteIdParaExclusao) {
            this.showError('ID do cliente não encontrado');
            return;
        }

        console.log('Executando exclusão do cliente ID:', this.clienteIdParaExclusao);

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            const response = await fetch(`/clientes/delete/${this.clienteIdParaExclusao}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();
            console.log('Resposta do servidor:', data);

            if (data.success) {
                this.showSuccess(data.message);
                this.fecharModal('excluirClienteModal');
                // Atualizar tabela dinamicamente
                setTimeout(() => {
                    this.atualizarTabela();
                }, 1000);
            } else {
                this.showError(data.message || 'Erro ao excluir cliente');
            }
        } catch (error) {
            console.error('Erro ao excluir cliente:', error);
            this.showError('Erro de conexão. Tente novamente.');
        }
    }

    preencherModalDetalhes(cliente) {
        console.log('Preenchendo modal de detalhes com:', cliente);

        const modal = document.getElementById('visualizarClienteModal');
        const body = modal.querySelector('#detalhesCliente');

        body.innerHTML = `
            <div class="row g-4">
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Nome da Empresa:</label>
                        <p class="info-value">${cliente.nome}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Nome Fantasia:</label>
                        <p class="info-value">${cliente.nome_fantasia || 'N/A'}</p>
                    </div>
                </div>
                <div class="col-12">
                    <div class="info-item">
                        <label class="info-label">Endereço:</label>
                        <p class="info-value">${cliente.endereco}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">CNPJ:</label>
                        <p class="info-value">
                            <span class="badge bg-info">${cliente.cnpj}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Comercial:</label>
                        <p class="info-value">${cliente.comercial || 'N/A'}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Tipo de Contrato:</label>
                        <p class="info-value">
                            <span class="badge bg-warning text-dark">${cliente.tipo_contrato || 'N/A'}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Início do Contrato:</label>
                        <p class="info-value">
                            <i class="fas fa-calendar-alt me-2 text-primary"></i>${cliente.inicio_de_contrato || 'N/A'}
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Quantidade em Contrato:</label>
                        <p class="info-value">${cliente.quantidade_em_contrato || 'N/A'}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Vigência:</label>
                        <p class="info-value">${cliente.vigencia || 'N/A'} meses</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Status:</label>
                        <p class="info-value">
                            <span class="badge ${cliente.status === 'Ativo' ? 'bg-success' : 'bg-secondary'}">${cliente.status || 'N/A'}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Término:</label>
                        <p class="info-value">${cliente.termino || 'N/A'}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Equipamento:</label>
                        <p class="info-value">
                            <span class="badge bg-secondary">${cliente.equipamento || 'N/A'}</span>
                        </p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Quantidade:</label>
                        <p class="info-value">${cliente.quantidade || 'N/A'}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">GR:</label>
                        <p class="info-value">${cliente.gr || 'N/A'}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Corretora:</label>
                        <p class="info-value">${cliente.corretora || 'N/A'}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Seguradora:</label>
                        <p class="info-value">${cliente.seguradora || 'N/A'}</p>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="info-item">
                        <label class="info-label">Data do Treinamento:</label>
                        <p class="info-value">
                            <i class="fas fa-calendar-alt me-2 text-primary"></i>${cliente.data_treinamento || 'N/A'}
                        </p>
                    </div>
                </div>
            </div>
        `;
    }

    preencherFormularioEdicao(cliente) {
        console.log('Preenchendo formulário de edição com:', cliente);

        // Preencher todos os campos
        const campos = [
            'nome', 'nome_fantasia', 'endereco', 'cnpj', 'comercial',
            'tipo_contrato', 'inicio_de_contrato', 'quantidade_em_contrato',
            'vigencia', 'status', 'termino', 'equipamento', 'quantidade',
            'gr', 'corretora', 'seguradora', 'data_treinamento'
        ];

        campos.forEach(campo => {
            const elemento = document.getElementById(`id_${campo}_edit`);
            if (elemento) {
                elemento.value = cliente[campo] || '';
            }
        });

        // Definir ID do cliente
        document.getElementById('cliente_id_edit').value = cliente.id;
    }

    aplicarFiltros() {
        const filtroNome = document.getElementById('filtroNome').value.toLowerCase();
        const filtroCnpj = document.getElementById('filtroCnpj').value.toLowerCase();
        const filtroStatus = document.getElementById('filtroStatus').value;

        const linhas = document.querySelectorAll('#tabelaClientes tbody tr');
        let visiveis = 0;

        linhas.forEach(linha => {
            const nome = linha.cells[1]?.textContent?.toLowerCase() || '';
            const cnpj = linha.cells[2]?.textContent?.toLowerCase() || '';
            const status = linha.cells[3]?.textContent?.toLowerCase() || '';

            const matchNome = !filtroNome || nome.includes(filtroNome);
            const matchCnpj = !filtroCnpj || cnpj.includes(filtroCnpj);
            const matchStatus = !filtroStatus || status.includes(filtroStatus.toLowerCase());

            if (matchNome && matchCnpj && matchStatus) {
                linha.style.display = '';
                visiveis++;
            } else {
                linha.style.display = 'none';
            }
        });

        // Atualizar contador
        const contador = document.getElementById('totalClientes');
        if (contador) {
            contador.textContent = visiveis;
        }
    }

    limparFiltros() {
        document.getElementById('filtroNome').value = '';
        document.getElementById('filtroCnpj').value = '';
        document.getElementById('filtroStatus').value = '';
        this.aplicarFiltros();
    }

    limparFormularios(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
            }
        }
    }

    abrirModal(modalId) {
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    fecharModal(modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        if (modal) {
            modal.hide();
        }
    }

    showLoading(element) {
        element.classList.add('loading');
        element.style.pointerEvents = 'none';
    }

    hideLoading(element) {
        element.classList.remove('loading');
        element.style.pointerEvents = '';
    }

    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'danger');
    }

    showInfo(message) {
        this.showAlert(message, 'info');
    }

    showAlert(message, type) {
        // Remover alertas existentes
        const existingAlerts = document.querySelectorAll('.alert-clientes');
        existingAlerts.forEach(alert => alert.remove());
        
        // Criar novo alerta
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show alert-clientes`;
        alert.style.position = 'fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '1000002';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // Remover automaticamente após 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }


    mostrarErrosFormulario(erros) {
        console.log('Erros do formulário:', erros);
        // Implementar exibição de erros específicos nos campos
    }

    async atualizarTabela() {
        console.log('🔄 Atualizando tabela de clientes...');
        
        try {
            // Mostrar loading
            this.showInfo('Atualizando lista de clientes...');
            
            // Recarregar apenas a tabela via AJAX
            const response = await fetch('/clientes/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            console.log('📡 Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const html = await response.text();
            console.log('📄 HTML recebido:', html.length, 'caracteres');
            
            // Extrair apenas a tabela do HTML retornado
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const novaTabela = doc.querySelector('#tabelaClientes');
            const contador = doc.querySelector('#totalClientes');
            
            console.log('🔍 Nova tabela encontrada:', !!novaTabela);
            console.log('🔍 Contador encontrado:', !!contador);
            
            if (novaTabela) {
                const tabelaAtual = document.querySelector('#tabelaClientes');
                if (tabelaAtual) {
                    console.log('✅ Atualizando conteúdo da tabela...');
                    tabelaAtual.innerHTML = novaTabela.innerHTML;
                    console.log('✅ Tabela atualizada com sucesso!');
                } else {
                    console.error('❌ Tabela atual não encontrada no DOM');
                }
            } else {
                console.error('❌ Nova tabela não encontrada no HTML retornado');
                console.log('📄 HTML completo:', html);
            }
            
            if (contador) {
                const contadorAtual = document.querySelector('#totalClientes');
                if (contadorAtual) {
                    console.log('🔢 Atualizando contador...');
                    contadorAtual.textContent = contador.textContent;
                    console.log('🔢 Contador atualizado:', contador.textContent);
                } else {
                    console.error('❌ Contador atual não encontrado no DOM');
                }
            } else {
                console.error('❌ Contador não encontrado no HTML retornado');
            }
            
            // Reaplicar filtros se houver
            console.log('🔍 Reaplicando filtros...');
            this.aplicarFiltros();
            console.log('✅ Tabela atualizada com sucesso!');
            
        } catch (error) {
            console.error('❌ Erro ao atualizar tabela:', error);
            console.error('❌ Stack trace:', error.stack);
            
            this.showError('Erro ao atualizar tabela. Recarregando página...');
            
            // Fallback: recarregar página se AJAX falhar
            setTimeout(() => {
                console.log('🔄 Fazendo fallback para reload da página...');
                window.location.reload();
            }, 2000);
        }
    }
}

// Funções globais para exportar e imprimir
function exportarDados() {
    console.log('Exportando dados de clientes...');
    
    const tabela = document.getElementById('tabelaClientes');
    const linhas = tabela.querySelectorAll('tbody tr');
    
    let dadosCSV = 'ID,Nome,Nome Fantasia,CNPJ,Status,Contrato,Equipamento,Início Contrato,Vigência,Quantidade,Corretora,Seguradora\n';
    
    linhas.forEach(linha => {
        if (linha.style.display !== 'none') {
            const colunas = linha.querySelectorAll('td');
            if (colunas.length > 0) {
                const id = colunas[0]?.textContent?.trim() || '';
                const nome = colunas[1]?.querySelector('strong')?.textContent?.trim() || '';
                const nomeFantasia = colunas[1]?.querySelector('.small')?.textContent?.trim() || '';
                const cnpj = colunas[2]?.textContent?.trim() || '';
                const status = colunas[3]?.textContent?.trim() || '';
                const contrato = colunas[4]?.textContent?.trim() || '';
                const equipamento = colunas[5]?.textContent?.trim() || '';
                const inicio = colunas[6]?.textContent?.trim() || '';
                const vigencia = colunas[7]?.textContent?.trim() || '';
                const quantidade = colunas[8]?.textContent?.trim() || '';
                const seguro = colunas[9]?.textContent?.trim() || '';
                
                dadosCSV += `"${id}","${nome}","${nomeFantasia}","${cnpj}","${status}","${contrato}","${equipamento}","${inicio}","${vigencia}","${quantidade}","${seguro}"\n`;
            }
        }
    });
    
    const blob = new Blob([dadosCSV], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `clientes_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    console.log('Dados exportados com sucesso!');
}

function imprimirTabela() {
    console.log('Preparando para impressão...');
    
    const janelaImpressao = window.open('', '_blank');
    const tabela = document.getElementById('tabelaClientes');
    
    janelaImpressao.document.write(`
        <html>
            <head>
                <title>Relatório de Clientes - ${new Date().toLocaleDateString()}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; text-align: center; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; font-weight: bold; }
                    .badge { padding: 2px 6px; border-radius: 3px; font-size: 12px; }
                    .bg-success { background-color: #28a745; color: white; }
                    .bg-secondary { background-color: #6c757d; color: white; }
                    .bg-info { background-color: #17a2b8; color: white; }
                    .bg-warning { background-color: #ffc107; color: black; }
                    @media print { body { margin: 0; } }
                </style>
            </head>
            <body>
                <h1>Relatório de Clientes</h1>
                <p><strong>Data:</strong> ${new Date().toLocaleDateString()}</p>
                <p><strong>Total de Clientes:</strong> ${document.getElementById('totalClientes').textContent}</p>
                ${tabela.outerHTML}
            </body>
        </html>
    `);
    
    janelaImpressao.document.close();
    janelaImpressao.print();
    
    console.log('Impressão iniciada!');
}

// Funções globais para compatibilidade
function aplicarFiltros() {
    if (window.clientesManager) {
        window.clientesManager.aplicarFiltros();
    }
}

function limparFiltros() {
    if (window.clientesManager) {
        window.clientesManager.limparFiltros();
    }
}

function visualizarCliente(id) {
    if (window.clientesManager) {
        window.clientesManager.visualizarCliente(id);
    }
}

function editarCliente(id) {
    if (window.clientesManager) {
        window.clientesManager.editarCliente(id);
    }
}

function excluirCliente(id) {
    if (window.clientesManager) {
        window.clientesManager.excluirCliente(id);
    }
}

function buscarClientes() {
    console.log('Buscando clientes...');
    if (window.clientesManager) {
        window.clientesManager.aplicarFiltros();
    }
}


// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 DOM carregado - Inicializando ClientesManager');
    window.clientesManager = new ClientesManager();
    console.log('✅ ClientesManager inicializado');
    console.log('🔧 ClientesManager disponível em window.clientesManager:', !!window.clientesManager);
});
