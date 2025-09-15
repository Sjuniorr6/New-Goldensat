# Configurações de Segurança - Golden SAT

## 🔒 Configurações Implementadas

### 1. Variáveis de Ambiente
- **SECRET_KEY**: Chave secreta do Django (nunca commitar)
- **DEBUG**: Modo debug (False em produção)
- **ALLOWED_HOSTS**: Hosts permitidos
- **EMAIL_***: Configurações de email

### 2. Proteções de Segurança
- ✅ **XSS Protection**: `SECURE_BROWSER_XSS_FILTER`
- ✅ **Content Type Sniffing**: `SECURE_CONTENT_TYPE_NOSNIFF`
- ✅ **Clickjacking Protection**: `X_FRAME_OPTIONS = 'DENY'`
- ✅ **HSTS**: HTTP Strict Transport Security
- ✅ **CSRF Protection**: Cookies seguros
- ✅ **Session Security**: Cookies HTTPOnly e Secure

### 3. Arquivos de Configuração
- `.gitignore`: Ignora arquivos sensíveis
- `.env`: Variáveis de ambiente (não commitar)
- `env.example`: Exemplo de configuração
- `security_config.py`: Configurações adicionais

## 🚀 Como Usar

### 1. Configurar Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
nano .env
```

### 2. Configurações Recomendadas para Produção
```env
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
```

### 3. Configurações de Email (Opcional)
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

## ⚠️ Importante

### Nunca Commitar:
- `.env`
- `db.sqlite3`
- `*.log`
- `__pycache__/`
- Arquivos com senhas ou chaves

### Em Produção:
1. Altere o SECRET_KEY
2. Configure DEBUG=False
3. Use HTTPS
4. Configure ALLOWED_HOSTS corretamente
5. Use banco de dados seguro (PostgreSQL/MySQL)

## 🔧 Comandos Úteis

### Gerar Nova SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Verificar Configurações de Segurança
```bash
python manage.py check --deploy
```

### Criar Backup do Banco
```bash
python manage.py dumpdata > backup.json
```

## 📝 Logs de Segurança

Os logs são salvos em:
- `logs/django.log`: Logs gerais do Django
- Console: Logs em tempo real

## 🛡️ Próximos Passos

1. **Rate Limiting**: Implementar limitação de tentativas
2. **2FA**: Autenticação de dois fatores
3. **Backup Automático**: Sistema de backup
4. **Monitoramento**: Logs de segurança
5. **Firewall**: Configurações de rede

## 📞 Suporte

Para dúvidas sobre segurança, consulte:
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
