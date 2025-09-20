# 🔍 VERIFICAR LOGS CORRETOS DO uWSGI

## ✅ **STATUS ATUAL:**
- ✅ uWSGI está rodando (11 processos)
- ✅ Socket existe: `/var/www/New-Goldensat/gserp.sock`
- ✅ Git pull foi feito com sucesso
- ✅ Serviços foram reiniciados

## 🔍 **VERIFICAR LOGS CORRETOS:**

### **1. Verificar logs do uWSGI (local correto):**
```bash
sudo tail -f /var/log/uwsgi/app/New-Golden.log
```

### **2. Verificar logs do Nginx:**
```bash
sudo tail -f /var/log/nginx/error.log
```

### **3. Testar o site:**
```bash
curl -I https://gserp.com.br
```

### **4. Se ainda der erro 500, verificar logs do Django:**
```bash
tail -f /var/www/New-Goldensat/logs/django.log
```

## 🎯 **COMANDOS EM SEQUÊNCIA:**

```bash
# 1. Verificar logs do uWSGI
sudo tail -f /var/log/uwsgi/app/New-Golden.log

# 2. Em outro terminal, testar o site
curl -I https://gserp.com.br

# 3. Se der erro, verificar logs do Nginx
sudo tail -f /var/log/nginx/error.log
```

## 🚀 **SE O SITE ESTIVER FUNCIONANDO:**

Acesse: https://gserp.com.br

Verifique se:
- ✅ Página carrega sem erro 500
- ✅ CSS/JS estão funcionando
- ✅ Imagens estão carregando
- ✅ Layout está correto

## 🆘 **SE AINDA DER ERRO:**

### **Verificar se o arquivo .env existe:**
```bash
cd /var/www/New-Goldensat
ls -la .env
```

### **Se não existir, criar:**
```bash
cat > .env << EOF
DEBUG=False
SECRET_KEY=django-insecure-7=sd^vwv+in5&os2t1zv00*#n#hr85rssdgj7b6kv%g36s#p@^
ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br,127.0.0.1
EOF
```

### **Reiniciar uWSGI:**
```bash
sudo systemctl restart uwsgi
```

**Execute os comandos e me diga o resultado!**
