// Função para abrir modal de detalhes
async function abrirModalDetalhes(id) {
    console.log('Abrindo detalhes da requisição:', id);
    
    try {
        const response = await fetch('/requisicoes/detail/' + id + '/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            const html = await response.text();
            document.getElementById('detalhesContent').innerHTML = html;
            
            const modal = new bootstrap.Modal(document.getElementById('detalhesModal'));
            modal.show();
        } else {
            console.error('Erro ao carregar detalhes:', response.status);
            alert('Erro ao carregar detalhes da requisição');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro interno: ' + error.message);
    }
}

// Função para abrir modal de edição
async function abrirModalEdicao(id) {
    console.log('Abrindo edição da requisição:', id);
    
    try {
        const response = await fetch('/requisicoes/update/' + id + '/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        if (response.ok) {
            const html = await response.text();
            document.getElementById('edicaoContent').innerHTML = html;
            
            const modal = new bootstrap.Modal(document.getElementById('edicaoModal'));
            modal.show();
            
            // Configurar o formulário de edição
            configurarFormularioEdicao();
        } else {
            console.error('Erro ao carregar formulário:', response.status);
            alert('Erro ao carregar formulário de edição');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro interno: ' + error.message);
    }
}

// Função para configurar o formulário de edição
function configurarFormularioEdicao() {
    const form = document.getElementById('editarRequisicaoForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            await salvarEdicao();
        });
    }
}

// Função para salvar edição
async function salvarEdicao() {
    console.log('Salvando edição...');
    
    const form = document.getElementById('editarRequisicaoForm');
    if (!form) {
        alert('Formulário não encontrado');
        return;
    }
    
    const formData = new FormData(form);
    
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('edicaoModal'));
            modal.hide();
            // Recarregar a página para mostrar as alterações
            location.reload();
        } else {
            alert('Erro: ' + data.message);
            if (data.errors) {
                console.error('Erros de validação:', data.errors);
            }
        }
    } catch (error) {
        console.error('Erro ao salvar:', error);
        alert('Erro interno: ' + error.message);
    }
}

// Função para abrir modal de exclusão
function abrirModalExclusao(id) {
    console.log('Abrindo confirmação de exclusão:', id);
    
    // Armazenar o ID para uso posterior
    window.requisicaoParaExcluir = id;
    
    const modal = new bootstrap.Modal(document.getElementById('exclusaoModal'));
    modal.show();
    
    // Configurar o botão de confirmação
    const confirmarBtn = document.getElementById('confirmarExclusaoBtn');
    confirmarBtn.onclick = function() {
        excluirRequisicao(id);
        modal.hide();
    };
}

// Função para excluir requisição
async function excluirRequisicao(id) {
    console.log('Excluindo requisição:', id);
    
    try {
        const response = await fetch('/requisicoes/delete/' + id + '/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();
        
        if (data.success) {
            // Remover o card da tela
            const card = document.querySelector('[data-id="' + id + '"]');
            if (card) {
                card.remove();
            }
            alert(data.message);
        } else {
            alert('Erro: ' + data.message);
        }
    } catch (error) {
        console.error('Erro ao excluir:', error);
        alert('Erro interno: ' + error.message);
    }
}

// Função para editar requisição (chamada do modal de detalhes)
function editarRequisicao(id) {
    // Fechar modal de detalhes
    const detalhesModal = bootstrap.Modal.getInstance(document.getElementById('detalhesModal'));
    detalhesModal.hide();
    
    // Abrir modal de edição
    setTimeout(() => {
        abrirModalEdicao(id);
    }, 300);
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    console.log('Página de configurações carregada');
    
    // Configurar tooltips se existirem
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
