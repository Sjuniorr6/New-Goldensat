import logging
import os
from django.conf import settings

def setup_logger(name, log_file, level=logging.DEBUG):
    """Configura um logger específico para salvar em arquivo"""
    
    try:
        # Criar o diretório de logs se não existir
        log_dir = os.path.join(settings.BASE_DIR, '..', 'log')
        os.makedirs(log_dir, exist_ok=True)
        
        # Caminho completo do arquivo de log
        log_path = os.path.join(log_dir, log_file)
        
        # Configurar o logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Evitar duplicação de handlers
        if logger.handlers:
            return logger
        
        # Handler para arquivo
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(level)
        
        # Formato das mensagens
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Adicionar handler ao logger
        logger.addHandler(file_handler)
        
        # Adicionar handler para console também (para debug)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Log inicial para confirmar que está funcionando
        logger.info("=" * 50)
        logger.info("LOGGER INICIALIZADO COM SUCESSO")
        logger.info(f"Arquivo de log: {log_path}")
        logger.info("=" * 50)
        
        return logger
        
    except Exception as e:
        # Fallback para console se houver erro
        print(f"Erro ao configurar logger: {e}")
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        return logger

# Logger específico para produtos - sempre funcionando
try:
    produtos_logger = setup_logger('produtos', 'app.log')
except Exception as e:
    # Fallback se houver qualquer erro
    produtos_logger = logging.getLogger('produtos')
    produtos_logger.setLevel(logging.DEBUG)
    if not produtos_logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        produtos_logger.addHandler(console_handler)
