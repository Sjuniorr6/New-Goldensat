# 🚨 ERRO 502 BAD GATEWAY - CORREÇÃO

## 🔥 **PROBLEMA:**
```
502 Bad Gateway
nginx/1.24.0 (Ubuntu)
```

**Causa:** Nginx não consegue se comunicar com o uWSGI.

## 🔍 **DIAGNÓSTICO:**

### **1. Verificar se o uWSGI está rodando:**
```bash
sudo systemctl status uwsgi
```

### **2. Verificar se o socket existe:**
```bash
ls -la /var/www/New-Goldensat/gserp.sock
```

### **3. Verificar logs do uWSGI:**
```bash
sudo tail -f /var/log/uwsgi/app/gserp.log
```

### **4. Verificar logs do Nginx:**
```bash
sudo tail -f /var/log/nginx/error.log
```

## ✅ **SOLUÇÕES:**

### **Solução 1: Reiniciar uWSGI**
```bash
sudo systemctl restart uwsgi
sudo systemctl status uwsgi
```

### **Solução 2: Se o uWSGI não iniciar, verificar configuração**
```bash
# Verificar se o arquivo de configuração existe
ls -la /etc/uwsgi/apps-available/gserp.ini

# Verificar se está habilitado
ls -la /etc/uwsgi/apps-enabled/gserp.ini
```

### **Solução 3: Verificar permissões do socket**
```bash
sudo chown -R www-data:www-data /var/www/New-Goldensat/
sudo chmod -R 755 /var/www/New-Goldensat/
```

### **Solução 4: Verificar se o arquivo .env existe**
```bash
cd /var/www/New-Goldensat
ls -la .env
```

Se não existir, criar:
```bash
cat > .env << EOF
DEBUG=False
SECRET_KEY=django-insecure-7=sd^vwv+in5&os2t1zv00*#n#hr85rssdgj7b6kv%g36s#p@^
ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br,127.0.0.1
EOF
```

### **Solução 5: Testar Django diretamente**
```bash
cd /var/www/New-Goldensat
source venv/bin/activate
python manage.py check --deploy
```

## 🚀 **COMANDOS EM SEQUÊNCIA:**

```bash
# 1. Verificar status
sudo systemctl status uwsgi

# 2. Reiniciar uWSGI
sudo systemctl restart uwsgi

# 3. Verificar se iniciou
sudo systemctl status uwsgi

# 4. Verificar socket
ls -la /var/www/New-Goldensat/gserp.sock

# 5. Verificar logs
sudo tail -f /var/log/uwsgi/app/gserp.log

# 6. Testar site
curl -I https://gserp.com.br
```

## 🆘 **SE AINDA NÃO FUNCIONAR:**

### **Verificar configuração do uWSGI:**
```bash
cat /etc/uwsgi/apps-available/gserp.ini
```

### **Verificar se o Python está funcionando:**
```bash
cd /var/www/New-Goldensat
source venv/bin/activate
python -c "import django; print(django.get_version())"
```

### **Verificar se o Django está funcionando:**
```bash
python manage.py check
```

**Execute os comandos em sequência até resolver!**
