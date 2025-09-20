# 🚨 CORREÇÃO DE EMERGÊNCIA - Golden SAT

## 🔥 **PROBLEMA CRÍTICO IDENTIFICADO:**

As configurações de segurança estavam muito restritivas e bloqueando o carregamento de recursos.

## ✅ **CORREÇÕES APLICADAS:**

### **1. Configurações de Segurança MÍNIMAS:**
```python
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
X_FRAME_OPTIONS = None
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = None
```

### **2. DEBUG = False (Produção)**
### **3. URLs de arquivos estáticos corretas**
### **4. MEDIA_ROOT corrigido**

## 🚀 **COMANDOS URGENTES NO SERVIDOR:**

```bash
# 1. Fazer pull das correções
cd /var/www/New-Goldensat
git pull origin main

# 2. Reiniciar serviços
sudo systemctl restart nginx
sudo systemctl restart uwsgi

# 3. Verificar se o arquivo .env existe e está correto
cat .env
```

## 📝 **SE NÃO EXISTIR .env, CRIAR:**

```bash
cd /var/www/New-Goldensat
cat > .env << EOF
DEBUG=False
SECRET_KEY=django-insecure-7=sd^vwv+in5&os2t1zv00*#n#hr85rssdgj7b6kv%g36s#p@^
ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br,127.0.0.1
EOF
```

## 🔍 **VERIFICAÇÕES CRÍTICAS:**

### **1. Verificar logs do Nginx:**
```bash
sudo tail -f /var/log/nginx/error.log
```

### **2. Verificar logs do uWSGI:**
```bash
sudo tail -f /var/log/uwsgi/app/gserp.log
```

### **3. Verificar se os arquivos existem:**
```bash
ls -la /var/www/staticfiles/
ls -la /var/www/New-Goldensat/media/
```

### **4. Testar manualmente:**
```bash
# Testar se o Django está funcionando
cd /var/www/New-Goldensat
source venv/bin/activate
python manage.py check --deploy
```

## 🆘 **SE AINDA NÃO FUNCIONAR:**

### **1. Verificar se o uWSGI está rodando:**
```bash
sudo systemctl status uwsgi
```

### **2. Verificar se o Nginx está rodando:**
```bash
sudo systemctl status nginx
```

### **3. Verificar se o socket existe:**
```bash
ls -la /var/www/New-Goldensat/gserp.sock
```

### **4. Verificar permissões:**
```bash
sudo chown -R www-data:www-data /var/www/New-Goldensat/
sudo chmod -R 755 /var/www/New-Goldensat/
```

## 🎯 **TESTE FINAL:**

1. Acessar: https://gserp.com.br
2. Verificar se a página carrega
3. Verificar se CSS/JS carregam (F12 > Network)
4. Verificar se não há erros no console

## ⚠️ **IMPORTANTE:**

- As configurações de segurança estão MÍNIMAS temporariamente
- Após funcionar, podemos reativar gradualmente
- O foco agora é fazer funcionar primeiro
