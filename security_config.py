"""
Configurações de segurança adicionais para o projeto Golden SAT
"""

import os
from django.conf import settings

# Configurações de segurança para produção
PRODUCTION_SECURITY_SETTINGS = {
    # HTTPS
    'SECURE_SSL_REDIRECT': True,
    'SECURE_PROXY_SSL_HEADER': ('HTTP_X_FORWARDED_PROTO', 'https'),
    
    # Cookies seguros
    'SESSION_COOKIE_SECURE': True,
    'CSRF_COOKIE_SECURE': True,
    
    # Headers de segurança
    'SECURE_BROWSER_XSS_FILTER': True,
    'SECURE_CONTENT_TYPE_NOSNIFF': True,
    'X_FRAME_OPTIONS': 'DENY',
    
    # HSTS
    'SECURE_HSTS_SECONDS': 31536000,  # 1 ano
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': True,
    'SECURE_HSTS_PRELOAD': True,
    
    # Referrer Policy
    'SECURE_REFERRER_POLICY': 'strict-origin-when-cross-origin',
}

# Configurações de desenvolvimento
DEVELOPMENT_SECURITY_SETTINGS = {
    'SECURE_SSL_REDIRECT': False,
    'SESSION_COOKIE_SECURE': False,
    'CSRF_COOKIE_SECURE': False,
    'SECURE_HSTS_SECONDS': 0,
}

def get_security_settings():
    """
    Retorna as configurações de segurança baseadas no ambiente
    """
    if settings.DEBUG:
        return DEVELOPMENT_SECURITY_SETTINGS
    else:
        return PRODUCTION_SECURITY_SETTINGS

# Lista de IPs permitidos para admin (opcional)
ALLOWED_ADMIN_IPS = [
    '127.0.0.1',
    'localhost',
    # Adicione outros IPs confiáveis aqui
]

# Configurações de rate limiting (opcional)
RATE_LIMIT_SETTINGS = {
    'LOGIN_ATTEMPTS': 5,  # Tentativas de login por IP
    'LOGIN_TIMEOUT': 300,  # 5 minutos
    'API_RATE_LIMIT': 100,  # Requests por hora
}

# Configurações de backup
BACKUP_SETTINGS = {
    'ENABLED': True,
    'FREQUENCY': 'daily',  # daily, weekly, monthly
    'RETENTION_DAYS': 30,
    'BACKUP_PATH': os.path.join(settings.BASE_DIR, 'backups'),
}
