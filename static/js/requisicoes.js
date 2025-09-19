/**
 * Sistema de Gerenciamento de Requisições - Golden SAT
 * JavaScript otimizado e moderno
 */

class RequisicoesManager {
    constructor() {
        this.requisicaoParaExcluir = null;
        this.init();
        this.setupEventListeners();
        console.log('✅ RequisicoesManager inicializado');
    }

    init() {
        console.log('🔧 Inicializando RequisicoesManager...');
        this.carregarClientes();
        this.setupModalEventListeners();
    }

    setupEventListeners() {
        console.log('🎯 Configurando event listeners...');
        
        // Formulários
        this.setupFormListeners();
        
        // Verificação de estoque
        this.setupEstoqueListeners();
        
        // Botão de exclusão
        this.setupExclusaoListener();
        
        // Filtros
        this.setupFiltrosListeners();
    }

    setupFormListeners() {
        const cadastrarForm = document.getElementById('requisicaoForm');
        if (cadastrarForm) {
            cadastrarForm.addEventListener('submit', (e) => this.handleSubmit(e, 'cadastrar'));
        }

        const editarForm = document.getElementById('editarRequisicaoForm');
        if (editarForm) {
            editarForm.addEventListener('submit', (e) => this.handleSubmit(e, 'editar'));
        }
    }

    setupEstoqueListeners() {
        const tipoProdutoSelect = document.querySelector('#id_tipo_produto');
        const quantidadeInput = document.querySelector('#id_numero_de_equipamentos');
        
        if (tipoProdutoSelect && quantidadeInput) {
            tipoProdutoSelect.addEventListener('change', () => this.verificarEstoque());
            quantidadeInput.addEventListener('input', () => this.verificarEstoque());
        }
    }

    setupExclusaoListener() {
        const confirmarExclusaoBtn = document.getElementById('confirmarExclusaoBtn');
        if (confirmarExclusaoBtn) {
            confirmarExclusaoBtn.addEventListener('click', () => this.executarExclusao());
        }
    }

    setupFiltrosListeners() {
        console.log('🔍 Configurando listeners dos filtros...');
        
        // Apenas configurar o indicador de filtros ativos
        const searchInput = document.getElementById('search');
        const clienteSelect = document.getElementById('cliente');
        
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                this.atualizarIndicadorFiltros();
            });
            
            // Permitir buscar pressionando Enter
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    aplicarFiltros();
                }
            });
        }
        
        if (clienteSelect) {
            clienteSelect.addEventListener('change', () => {
                this.atualizarIndicadorFiltros();
            });
        }
    }

    atualizarIndicadorFiltros() {
        const searchInput = document.getElementById('search');
        const clienteSelect = document.getElementById('cliente');
        const filtersCard = document.querySelector('.filters-card');
        
        if (filtersCard) {
            const temFiltrosAtivos = (searchInput?.value || '') || (clienteSelect?.value || '');
            
            if (temFiltrosAtivos) {
                filtersCard.classList.add('filters-active');
            } else {
                filtersCard.classList.remove('filters-active');
            }
        }
    }

    setupModalEventListeners() {
        const modals = ['cadastrarRequisicaoModal', 'editarRequisicaoModal', 'detalhesRequisicaoModal'];
        
        modals.forEach(modalId => {
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.addEventListener('hidden.bs.modal', () => {
                    this.limparFormularios();
                    this.ocultarAlertas();
                });
            }
        });
    }

    async carregarClientes() {
        try {
            console.log('📋 Carregando lista de clientes...');
            
            // Mostrar loading no select
            this.mostrarLoadingClientes();
            
            // Timeout de 10 segundos
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000);
            
            const response = await fetch('/clientes/api/clientes/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.clientes) {
                    this.preencherSelectClientes(data.clientes);
                    console.log(`✅ ${data.total} clientes carregados com sucesso`);
                } else {
                    console.error('❌ Erro na resposta da API:', data.message);
                    this.mostrarErroClientes(data.message || 'Erro ao carregar clientes');
                }
            } else {
                console.error('❌ Erro HTTP:', response.status, response.statusText);
                this.mostrarErroClientes(`Erro HTTP: ${response.status}`);
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                console.error('❌ Timeout ao carregar clientes');
                this.mostrarErroClientes('Timeout - tente novamente');
            } else {
                console.error('❌ Erro ao carregar clientes:', error);
                this.mostrarErroClientes('Erro de conexão');
            }
        } finally {
            this.ocultarLoadingClientes();
        }
    }

    preencherSelectClientes(clientes) {
        const selectCliente = document.getElementById('cliente');
        if (selectCliente) {
            // Limpar opções existentes (exceto a primeira "Todos os Clientes")
            while (selectCliente.children.length > 1) {
                selectCliente.removeChild(selectCliente.lastChild);
            }

            // Adicionar clientes
            if (clientes && clientes.length > 0) {
                clientes.forEach(cliente => {
                    const option = document.createElement('option');
                    option.value = cliente.id;
                    
                    // Mostrar apenas o nome do cliente (mais compacto)
                    let displayText = cliente.cliente;
                    
                    // Se o nome for muito longo, truncar
                    if (displayText.length > 20) {
                        displayText = displayText.substring(0, 17) + '...';
                    }
                    
                    option.textContent = displayText;
                    option.title = `${cliente.cliente} | CNPJ: ${cliente.cnpj || 'Não informado'} | Status: ${cliente.status || 'Não informado'}`;
                    selectCliente.appendChild(option);
                });
                console.log(`✅ ${clientes.length} clientes carregados no select`);
            } else {
                console.warn('⚠️ Nenhum cliente encontrado');
                // Adicionar opção de "Nenhum cliente cadastrado"
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'Nenhum cliente cadastrado';
                option.disabled = true;
                selectCliente.appendChild(option);
            }
        } else {
            console.error('❌ Select de cliente não encontrado');
        }
    }

    async verificarEstoque() {
        const tipoProdutoSelect = document.querySelector('#id_tipo_produto');
        const quantidadeInput = document.querySelector('#id_numero_de_equipamentos');
        const alertaEstoque = document.getElementById('alertaEstoque') || document.getElementById('alertaEstoqueEdicao');
        const mensagemEstoque = document.getElementById('mensagemEstoque') || document.getElementById('mensagemEstoqueEdicao');

        if (!tipoProdutoSelect || !quantidadeInput || !alertaEstoque || !mensagemEstoque) {
            return;
        }

        const produtoId = tipoProdutoSelect.value;
        const quantidade = quantidadeInput.value;

        if (!produtoId || !quantidade) {
            this.ocultarAlertaEstoque();
            return;
        }

        try {
            console.log(`🔍 Verificando estoque: Produto ${produtoId}, Quantidade ${quantidade}`);
            
            const formData = new FormData();
            formData.append('produto_id', produtoId);
            formData.append('quantidade', quantidade);
            formData.append('csrfmiddlewaretoken', this.getCSRFToken());

            const response = await fetch('/requisicoes/verificar-estoque-requisicao/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();
            
            if (data.success) {
                this.ocultarAlertaEstoque();
                console.log('✅ Estoque disponível:', data.estoque_disponivel);
            } else {
                this.mostrarAlertaEstoque(data.message);
                console.warn('⚠️ Estoque insuficiente:', data.message);
            }
        } catch (error) {
            console.error('❌ Erro ao verificar estoque:', error);
        }
    }

    mostrarAlertaEstoque(mensagem) {
        const alertaEstoque = document.getElementById('alertaEstoque') || document.getElementById('alertaEstoqueEdicao');
        const mensagemEstoque = document.getElementById('mensagemEstoque') || document.getElementById('mensagemEstoqueEdicao');
        
        if (alertaEstoque && mensagemEstoque) {
            mensagemEstoque.textContent = mensagem;
            alertaEstoque.classList.remove('d-none');
            alertaEstoque.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    ocultarAlertaEstoque() {
        const alertaEstoque = document.getElementById('alertaEstoque') || document.getElementById('alertaEstoqueEdicao');
        if (alertaEstoque) {
            alertaEstoque.classList.add('d-none');
        }
    }

    async handleSubmit(event, tipo) {
        event.preventDefault();
        console.log(`📝 Submetendo formulário: ${tipo}`);

        const form = event.target;
        const formData = new FormData(form);
        const url = tipo === 'cadastrar' ? '/requisicoes/cadastrar/' : `/requisicoes/update/${form.dataset.requisicaoId}/`;

        try {
            this.showLoading();

            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showSuccess(data.message);
                this.fecharModal(tipo);
                this.atualizarCards();
            } else {
                this.showError(data.message || 'Erro ao salvar requisição');
                if (data.errors) {
                    this.mostrarErrosValidacao(data.errors);
                }
            }
        } catch (error) {
            console.error('❌ Erro ao submeter formulário:', error);
            this.showError('Erro interno do servidor');
        } finally {
            this.hideLoading();
        }
    }

    async visualizarRequisicao(id) {
        try {
            console.log(`👁️ Visualizando requisição ${id}`);
            this.showLoading();

            const response = await fetch(`/requisicoes/detail/${id}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const html = await response.text();
                document.getElementById('detalhesRequisicaoContent').innerHTML = html;
                
                const modal = new bootstrap.Modal(document.getElementById('detalhesRequisicaoModal'));
                modal.show();
            } else {
                this.showError('Erro ao carregar detalhes da requisição');
            }
        } catch (error) {
            console.error('❌ Erro ao visualizar requisição:', error);
            this.showError('Erro interno do servidor');
        } finally {
            this.hideLoading();
        }
    }

    async editarRequisicao(id) {
        try {
            console.log(`✏️ Editando requisição ${id}`);
            this.showLoading();

            const response = await fetch(`/requisicoes/update/${id}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const html = await response.text();
                document.getElementById('editarRequisicaoContent').innerHTML = html;
                
                // Adicionar ID da requisição ao formulário
                const form = document.getElementById('editarRequisicaoForm');
                if (form) {
                    form.dataset.requisicaoId = id;
                }

                // Reconfigurar event listeners
                this.setupEventListeners();
                
                // Configurar controle de antenista APÓS o conteúdo ser carregado
                setTimeout(() => {
                    controlarVisibilidadeAntenista();
                }, 100);
                
                const modal = new bootstrap.Modal(document.getElementById('editarRequisicaoModal'));
                modal.show();
            } else {
                this.showError('Erro ao carregar requisição para edição');
            }
        } catch (error) {
            console.error('❌ Erro ao editar requisição:', error);
            this.showError('Erro interno do servidor');
        } finally {
            this.hideLoading();
        }
    }

    async excluirRequisicao(id) {
        console.log(`🗑️ Excluindo requisição ${id}`);
        this.requisicaoParaExcluir = id;
        
        const modal = new bootstrap.Modal(document.getElementById('excluirRequisicaoModal'));
        modal.show();
    }

    async executarExclusao() {
        if (!this.requisicaoParaExcluir) return;

        try {
            console.log(`🗑️ Executando exclusão da requisição ${this.requisicaoParaExcluir}`);
            this.showLoading();

            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', this.getCSRFToken());

            const response = await fetch(`/requisicoes/delete/${this.requisicaoParaExcluir}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showSuccess(data.message);
                this.fecharModal('excluir');
                this.atualizarCards();
            } else {
                this.showError(data.message || 'Erro ao excluir requisição');
            }
        } catch (error) {
            console.error('❌ Erro ao excluir requisição:', error);
            this.showError('Erro interno do servidor');
        } finally {
            this.hideLoading();
            this.requisicaoParaExcluir = null;
        }
    }

    async atualizarCards() {
        try {
            console.log('🔄 Atualizando cards de requisições...');
            
            // Mostrar loading
            this.mostrarLoadingCards();
            
            const params = new URLSearchParams();
            const search = document.getElementById('search')?.value || '';
            const cliente = document.getElementById('cliente')?.value || '';

            if (search) params.append('search', search);
            if (cliente) params.append('cliente', cliente);

            const url = `/requisicoes/?${params.toString()}`;
            
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Atualizar o grid de cards
                const novoGrid = doc.querySelector('#cardsGrid');
                const gridAtual = document.querySelector('#cardsGrid');
                
                if (novoGrid && gridAtual) {
                    gridAtual.innerHTML = novoGrid.innerHTML;
                    this.atualizarContador();
                    console.log('✅ Cards atualizados com sucesso');
                } else {
                    console.warn('⚠️ Grid não encontrado, recarregando página...');
                    window.location.reload();
                }
            } else {
                console.warn('⚠️ Erro ao atualizar cards, recarregando página...');
                window.location.reload();
            }
        } catch (error) {
            console.error('❌ Erro ao atualizar cards:', error);
            window.location.reload();
        } finally {
            this.ocultarLoadingCards();
        }
    }

    atualizarContador() {
        const cards = document.querySelectorAll('.card[data-id]');
        const contador = document.getElementById('totalRequisicoes');
        if (contador) {
            contador.textContent = cards.length;
        }
    }

    mostrarLoadingCards() {
        const grid = document.querySelector('#cardsGrid');
        if (grid) {
            grid.classList.add('cards-loading');
        }
    }

    ocultarLoadingCards() {
        const grid = document.querySelector('#cardsGrid');
        if (grid) {
            grid.classList.remove('cards-loading');
        }
    }

    mostrarLoadingClientes() {
        const selectCliente = document.getElementById('cliente');
        if (selectCliente) {
            selectCliente.disabled = true;
            selectCliente.innerHTML = '<option value="">Carregando clientes...</option>';
        }
    }

    ocultarLoadingClientes() {
        const selectCliente = document.getElementById('cliente');
        if (selectCliente) {
            selectCliente.disabled = false;
        }
    }

    mostrarErroClientes(mensagem) {
        const selectCliente = document.getElementById('cliente');
        if (selectCliente) {
            selectCliente.innerHTML = `<option value="">Erro: ${mensagem}</option>`;
        }
    }

    fecharModal(tipo) {
        const modalIds = {
            'cadastrar': 'cadastrarRequisicaoModal',
            'editar': 'editarRequisicaoModal',
            'detalhes': 'detalhesRequisicaoModal',
            'excluir': 'excluirRequisicaoModal'
        };

        const modalId = modalIds[tipo];
        if (modalId) {
            const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
            if (modal) {
                modal.hide();
            }
        }
    }

    limparFormularios() {
        const formularios = ['requisicaoForm', 'editarRequisicaoForm'];
        formularios.forEach(formId => {
            const form = document.getElementById(formId);
            if (form) {
                form.reset();
            }
        });
    }

    ocultarAlertas() {
        this.ocultarAlertaEstoque();
        const alertas = document.querySelectorAll('.alert');
        alertas.forEach(alerta => {
            if (alerta.id.includes('Estoque')) {
                alerta.classList.add('d-none');
            }
        });
    }

    mostrarErrosValidacao(errors) {
        console.log('⚠️ Erros de validação:', errors);
        
        // Limpar erros anteriores
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
        document.querySelectorAll('.invalid-feedback').forEach(el => {
            el.remove();
        });

        // Mostrar novos erros
        Object.keys(errors).forEach(field => {
            const input = document.querySelector(`[name="${field}"]`);
            if (input) {
                input.classList.add('is-invalid');
                
                const feedback = document.createElement('div');
                feedback.className = 'invalid-feedback';
                feedback.textContent = errors[field][0];
                input.parentNode.appendChild(feedback);
            }
        });
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    // Sistema de notificações
    showLoading() {
        const loadingHtml = `
            <div class="loading-overlay">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', loadingHtml);
    }

    hideLoading() {
        const loading = document.querySelector('.loading-overlay');
        if (loading) {
            loading.remove();
        }
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
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;" role="alert">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', alertHtml);
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            const alert = document.querySelector('.alert:last-of-type');
            if (alert) {
                alert.remove();
            }
        }, 5000);
    }
}

// Funções globais para compatibilidade com onclick
function aplicarFiltros() {
    if (window.requisicoesManager) {
        window.requisicoesManager.atualizarCards();
        window.requisicoesManager.atualizarIndicadorFiltros();
    }
}

function limparFiltros() {
    document.getElementById('search').value = '';
    document.getElementById('cliente').value = '';
    if (window.requisicoesManager) {
        window.requisicoesManager.atualizarCards();
        window.requisicoesManager.atualizarIndicadorFiltros();
    }
}

function visualizarRequisicao(id) {
    if (window.requisicoesManager) {
        window.requisicoesManager.visualizarRequisicao(id);
    }
}

function editarRequisicao(id) {
    if (window.requisicoesManager) {
        window.requisicoesManager.editarRequisicao(id);
    }
}

function excluirRequisicao(id) {
    if (window.requisicoesManager) {
        window.requisicoesManager.excluirRequisicao(id);
    }
}


function exportarDados() {
    console.log('📊 Exportando dados...');
    const cards = document.querySelectorAll('.requisicao-card');
    if (cards.length === 0) return;

    let csv = 'ID,Cliente,CNPJ,Produto,Quantidade,Valor Total,Status,Comercial,Motivo,Data\n';
    cards.forEach(card => {
        const id = card.querySelector('.badge-id')?.textContent.replace('#', '') || '';
        const cliente = card.querySelector('.client-name')?.textContent.trim() || '';
        const cnpj = card.querySelector('.client-cnpj')?.textContent.trim() || '';
        const produto = card.querySelector('.product-name')?.textContent.trim() || '';
        const quantidade = card.querySelector('.stat-value:not(.stat-price)')?.textContent.trim() || '';
        const valorTotal = card.querySelector('.stat-price')?.textContent.trim() || '';
        const status = card.querySelector('.badge-status')?.textContent.trim() || '';
        const comercial = card.querySelector('.info-text')?.textContent.trim() || '';
        const motivo = card.querySelectorAll('.info-text')[1]?.textContent.trim() || '';
        const data = card.querySelector('.card-date')?.textContent.trim() || '';
        
        csv += `"${id}","${cliente}","${cnpj}","${produto}","${quantidade}","${valorTotal}","${status}","${comercial}","${motivo}","${data}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `requisicoes_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function imprimirTabela() {
    console.log('🖨️ Imprimindo cards...');
    const cards = document.querySelectorAll('.requisicao-card');
    if (cards.length === 0) return;

    // Coletar HTML de todos os cards
    let cardsHTML = '';
    cards.forEach(card => {
        cardsHTML += card.outerHTML;
    });

    const janelaImpressao = window.open('', '_blank');
    janelaImpressao.document.write(`
        <html>
            <head>
                <title>Listagem de Requisições - Golden SAT</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .print-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
                    .print-card { border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 20px; }
                    .print-card-header { border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 15px; }
                    .print-card-body { margin-bottom: 15px; }
                    .print-card-footer { border-top: 1px solid #eee; padding-top: 10px; }
                    .badge { padding: 2px 6px; border-radius: 3px; font-size: 12px; margin-right: 5px; }
                    .bg-secondary { background-color: #6c757d; color: white; }
                    .bg-info { background-color: #17a2b8; color: white; }
                    .bg-warning { background-color: #ffc107; color: black; }
                    .bg-success { background-color: #28a745; color: white; }
                    .bg-danger { background-color: #dc3545; color: white; }
                    .text-primary { color: #007bff; }
                    .text-secondary { color: #6c757d; }
                    .text-success { color: #28a745; font-weight: bold; }
                    .fw-bold { font-weight: bold; }
                    .text-muted { color: #6c757d; }
                    .small { font-size: 0.875em; }
                    .mb-1 { margin-bottom: 0.25rem; }
                    .mb-3 { margin-bottom: 1rem; }
                    .row { display: flex; }
                    .col-6 { flex: 0 0 50%; }
                    .text-center { text-align: center; }
                    .d-flex { display: flex; }
                    .justify-content-between { justify-content: space-between; }
                    .align-items-center { align-items: center; }
                </style>
            </head>
            <body>
                <h1>Listagem de Requisições - Golden SAT</h1>
                <p>Data de impressão: ${new Date().toLocaleString('pt-BR')}</p>
                <div class="print-cards">
                    ${cardsHTML}
                </div>
            </body>
        </html>
    `);
    janelaImpressao.document.close();
    janelaImpressao.print();
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando sistema de requisições...');
    window.requisicoesManager = new RequisicoesManager();
    
    // Carregar modal de cadastro quando necessário
    const cadastrarModal = document.getElementById('cadastrarRequisicaoModal');
    if (cadastrarModal) {
        cadastrarModal.addEventListener('show.bs.modal', async function() {
            try {
                const response = await fetch('/requisicoes/cadastrar/', {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                if (response.ok) {
                    const html = await response.text();
                    document.getElementById('cadastrarRequisicaoContent').innerHTML = html;
                    
                    // Reconfigurar event listeners
                    window.requisicoesManager.setupEventListeners();
                    
                    // Configurar controle de antenista APÓS o conteúdo ser carregado
                    setTimeout(() => {
                        controlarVisibilidadeAntenista();
                    }, 100);
                }
            } catch (error) {
                console.error('❌ Erro ao carregar modal de cadastro:', error);
            }
        });
    }
    
    // Remover backdrop dos modais
    removerBackdropModais();
});

// Função para remover backdrop dos modais
function removerBackdropModais() {
    // Remover backdrop existente
    const backdrops = document.querySelectorAll('.modal-backdrop');
    backdrops.forEach(backdrop => {
        backdrop.remove();
    });
    
    // Observar mudanças no DOM para remover novos backdrops
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    if (node.classList && node.classList.contains('modal-backdrop')) {
                        node.remove();
                    }
                    // Verificar filhos também
                    const childBackdrops = node.querySelectorAll && node.querySelectorAll('.modal-backdrop');
                    if (childBackdrops) {
                        childBackdrops.forEach(backdrop => backdrop.remove());
                    }
                }
            });
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Função para controlar visibilidade do campo antenista
function controlarVisibilidadeAntenista() {
    // Função para modal de criação
    function setupAntenistaControl(modalId, antenistaFieldId) {
        const modal = document.getElementById(modalId);
        if (!modal) {
            console.log('❌ Modal não encontrado:', modalId);
            return;
        }
        
        const motivoSelect = modal.querySelector('select[name="motivo"]');
        const antenistaField = modal.querySelector(`#${antenistaFieldId}`);
        
        if (!motivoSelect || !antenistaField) {
            console.log('❌ Elementos não encontrados no modal:', modalId);
            return;
        }
        
        // Função para verificar e mostrar/ocultar campo
        function toggleAntenistaField() {
            const motivoValue = motivoSelect.value;
            console.log('🔍 Motivo selecionado:', motivoValue);
            
            if (motivoValue === 'Isca FAST') {
                console.log('✅ Mostrando campo antenista');
                antenistaField.style.display = 'block';
            } else {
                console.log('❌ Ocultando campo antenista');
                antenistaField.style.display = 'none';
            }
        }
        
        // Verificar quando o modal é aberto
        modal.addEventListener('shown.bs.modal', function() {
            toggleAntenistaField();
        });
        
        // Verificar quando o motivo muda
        motivoSelect.addEventListener('change', function() {
            toggleAntenistaField();
        });
        
        // Verificar inicialmente
        toggleAntenistaField();
    }
    
    // Configurar para ambos os modais
    setupAntenistaControl('cadastrarRequisicaoModal', 'antenista-field');
    setupAntenistaControl('editarRequisicaoModal', 'antenista-field-edit');
}

// Inicializar controle de antenista quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    controlarVisibilidadeAntenista();
});

// Re-inicializar quando novos modais forem carregados via AJAX
document.addEventListener('ajaxComplete', function() {
    controlarVisibilidadeAntenista();
});

// Função para aprovar requisição
async function aprovarRequisicao(id) {
    console.log(`🚀 Iniciando aprovação da requisição ${id}`);
    
    // Configurar modal de confirmação
    configurarModalConfirmacao(
        'fas fa-check-circle text-success',
        'Confirmar Aprovação',
        'Tem certeza que deseja <strong>APROVAR</strong> esta requisição?',
        'Esta ação mudará o status para "Aprovado pelo CEO"',
        'success',
        async () => {
            try {
                console.log(`📝 Preparando requisição para aprovar ID: ${id}`);
                
                // Tentar encontrar o token CSRF
                let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                if (!csrfToken) {
                    // Tentar encontrar em outros locais
                    csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
                }
                if (!csrfToken) {
                    // Tentar encontrar no meta tag
                    csrfToken = document.querySelector('meta[name="csrf-token"]');
                }
                
                const formData = new FormData();
                if (csrfToken) {
                    formData.append('csrfmiddlewaretoken', csrfToken.value);
                    console.log('✅ Token CSRF encontrado:', csrfToken.value.substring(0, 10) + '...');
                } else {
                    console.warn('⚠️ Token CSRF não encontrado, tentando sem ele');
                }
                
                console.log(`🌐 Enviando requisição para: /requisicoes/aprovar/${id}/`);
                
                const response = await fetch(`/requisicoes/aprovar/${id}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                console.log(`📡 Resposta recebida:`, response.status, response.statusText);
                
                if (!response.ok) {
                    console.error(`❌ Erro HTTP: ${response.status} - ${response.statusText}`);
                    const errorText = await response.text();
                    console.error('❌ Conteúdo da resposta de erro:', errorText);
                    window.requisicoesManager.showError(`Erro HTTP ${response.status}: ${response.statusText}`);
                    return;
                }
                
                const data = await response.json();
                console.log('📊 Dados da resposta:', data);
                
                if (data.success) {
                    console.log('✅ Requisição aprovada com sucesso');
                    window.requisicoesManager.showSuccess(data.message);
                    // Atualizar cor do card para verde claro
                    atualizarCorCard(id, 'approved');
                    window.requisicoesManager.atualizarCards();
                } else {
                    console.error('❌ Falha na aprovação:', data.message);
                    window.requisicoesManager.showError(data.message);
                }
            } catch (error) {
                console.error('❌ Erro ao aprovar requisição:', error);
                window.requisicoesManager.showError('Erro ao aprovar requisição: ' + error.message);
            }
        }
    );
}

// Função para reprovar requisição
async function reprovarRequisicao(id) {
    // Configurar modal de confirmação
    configurarModalConfirmacao(
        'fas fa-times-circle text-danger',
        'Confirmar Reprovação',
        'Tem certeza que deseja <strong>REPROVAR</strong> esta requisição?',
        'Esta ação mudará o status para "Reprovado pelo CEO"',
        'danger',
        async () => {
            try {
                console.log(`📝 Preparando requisição para reprovar ID: ${id}`);
                
                // Tentar encontrar o token CSRF
                let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                if (!csrfToken) {
                    // Tentar encontrar em outros locais
                    csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
                }
                if (!csrfToken) {
                    // Tentar encontrar no meta tag
                    csrfToken = document.querySelector('meta[name="csrf-token"]');
                }
                
                const formData = new FormData();
                if (csrfToken) {
                    formData.append('csrfmiddlewaretoken', csrfToken.value);
                    console.log('✅ Token CSRF encontrado:', csrfToken.value.substring(0, 10) + '...');
                } else {
                    console.warn('⚠️ Token CSRF não encontrado, tentando sem ele');
                }
                
                console.log(`🌐 Enviando requisição para: /requisicoes/reprovar/${id}/`);
                
                const response = await fetch(`/requisicoes/reprovar/${id}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                console.log(`📡 Resposta recebida:`, response.status, response.statusText);
                
                if (!response.ok) {
                    console.error(`❌ Erro HTTP: ${response.status} - ${response.statusText}`);
                    const errorText = await response.text();
                    console.error('❌ Conteúdo da resposta de erro:', errorText);
                    window.requisicoesManager.showError(`Erro HTTP ${response.status}: ${response.statusText}`);
                    return;
                }
                
                const data = await response.json();
                console.log('📊 Dados da resposta:', data);
                
                if (data.success) {
                    console.log('✅ Requisição reprovada com sucesso');
                    window.requisicoesManager.showSuccess(data.message);
                    // Atualizar cor do card para vermelho claro
                    atualizarCorCard(id, 'rejected');
                    window.requisicoesManager.atualizarCards();
                } else {
                    console.error('❌ Falha na reprovação:', data.message);
                    window.requisicoesManager.showError(data.message);
                }
            } catch (error) {
                console.error('❌ Erro ao reprovar requisição:', error);
                window.requisicoesManager.showError('Erro ao reprovar requisição: ' + error.message);
            }
        }
    );
}

// Função para atualizar a cor do card
function atualizarCorCard(id, status) {
    const card = document.querySelector(`[data-id="${id}"]`);
    if (card) {
        // Remover classes anteriores
        card.classList.remove('card-approved', 'card-rejected');
        
        // Adicionar nova classe baseada no status
        if (status === 'approved') {
            card.classList.add('card-approved');
        } else if (status === 'rejected') {
            card.classList.add('card-rejected');
        }
    }
}

// Função para configurar o modal de confirmação
function configurarModalConfirmacao(iconClass, title, message, subMessage, type, callback) {
    const modal = document.getElementById('confirmModal');
    const confirmIcon = document.getElementById('confirmIcon');
    const confirmTitle = document.getElementById('confirmTitle');
    const confirmMessage = document.getElementById('confirmMessage');
    const confirmSubMessage = document.getElementById('confirmSubMessage');
    const confirmButton = document.getElementById('confirmButton');
    
    // Configurar conteúdo
    confirmIcon.innerHTML = `<i class="${iconClass}"></i>`;
    confirmTitle.textContent = title;
    confirmMessage.innerHTML = message;
    confirmSubMessage.textContent = subMessage;
    
    // Configurar estilo baseado no tipo
    modal.classList.remove('reject-modal');
    if (type === 'danger') {
        modal.classList.add('reject-modal');
    }
    
    // Remover listeners anteriores
    const newConfirmButton = confirmButton.cloneNode(true);
    confirmButton.parentNode.replaceChild(newConfirmButton, confirmButton);
    
    // Adicionar novo listener
    newConfirmButton.addEventListener('click', () => {
        const bootstrapModal = bootstrap.Modal.getInstance(modal);
        bootstrapModal.hide();
        callback();
    });
    
    // Mostrar modal
    const bootstrapModal = new bootstrap.Modal(modal);
    bootstrapModal.show();
}

