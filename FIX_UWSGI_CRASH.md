# 🚨 CORREÇÃO DO CRASH DO uWSGI

## 🔥 **PROBLEMA IDENTIFICADO:**
```
upstream prematurely closed connection while reading response header from upstream
```

**Causa:** O uWSGI está crashando devido a um erro no Django.

## ✅ **SOLUÇÕES:**

### **1. Verificar se o arquivo .env está correto:**
```bash
cd /var/www/New-Goldensat
cat .env
```

### **2. Corrigir o .env (DEBUG=False):**
```bash
cd /var/www/New-Goldensat
cat > .env << EOF
DEBUG=False
SECRET_KEY=django-insecure-7=sd^vwv+in5&os2t1zv00*#n#hr85rssdgj7b6kv%g36s#p@^
ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br,127.0.0.1
EOF
```

### **3. Verificar se o arquivo settings.py está correto:**
```bash
grep -n "X_FRAME_OPTIONS" int/settings.py
```

Deve mostrar:
```
167:X_FRAME_OPTIONS = 'SAMEORIGIN'
```

### **4. Se não estiver correto, corrigir:**
```bash
sed -i "s/X_FRAME_OPTIONS = None/X_FRAME_OPTIONS = 'SAMEORIGIN'/g" int/settings.py
```

### **5. Testar Django diretamente:**
```bash
cd /var/www/New-Goldensat
source venv/bin/activate
python manage.py check
```

### **6. Se der erro, ativar DEBUG temporariamente:**
```bash
cd /var/www/New-Goldensat
cat > .env << EOF
DEBUG=True
SECRET_KEY=django-insecure-7=sd^vwv+in5&os2t1zv00*#n#hr85rssdgj7b6kv%g36s#p@^
ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br,127.0.0.1
EOF
```

### **7. Reiniciar uWSGI:**
```bash
sudo systemctl restart uwsgi
```

### **8. Verificar logs:**
```bash
sudo tail -f /var/log/uwsgi/app/New-Golden.log
```

## 🎯 **COMANDOS EM SEQUÊNCIA:**

```bash
# 1. Corrigir .env
cd /var/www/New-Goldensat
cat > .env << EOF
DEBUG=False
SECRET_KEY=django-insecure-7=sd^vwv+in5&os2t1zv00*#n#hr85rssdgj7b6kv%g36s#p@^
ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br,127.0.0.1
EOF

# 2. Verificar settings.py
grep -n "X_FRAME_OPTIONS" int/settings.py

# 3. Testar Django
source venv/bin/activate
python manage.py check

# 4. Reiniciar uWSGI
sudo systemctl restart uwsgi

# 5. Testar site
curl -I https://gserp.com.br
```

**Execute esses comandos em sequência!**
