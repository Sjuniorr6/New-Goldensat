# 🚨 CORREÇÃO URGENTE NO SERVIDOR

## 🔥 **PROBLEMAS IDENTIFICADOS:**

1. **Git com problema de permissões**
2. **Site ainda retornando erro 500**
3. **Configurações não foram aplicadas**

## ✅ **SOLUÇÃO IMEDIATA:**

### **1. Corrigir permissões do Git:**
```bash
cd /var/www/New-Goldensat
git config --global --add safe.directory /var/www/New-Goldensat
```

### **2. Fazer pull das alterações:**
```bash
git pull origin main
```

### **3. Se ainda não funcionar, corrigir manualmente:**
```bash
# Verificar o arquivo atual
grep -n "X_FRAME_OPTIONS" int/settings.py

# Se ainda estiver com None, corrigir:
sed -i "s/X_FRAME_OPTIONS = None/X_FRAME_OPTIONS = 'SAMEORIGIN'/g" int/settings.py
sed -i "s/CSRF_COOKIE_SAMESITE = None/CSRF_COOKIE_SAMESITE = 'Lax'/g" int/settings.py
sed -i "s/SESSION_COOKIE_SAMESITE = None/SESSION_COOKIE_SAMESITE = 'Lax'/g" int/settings.py
```

### **4. Verificar se foi corrigido:**
```bash
grep -n "X_FRAME_OPTIONS" int/settings.py
```

**Deve mostrar:**
```
167:X_FRAME_OPTIONS = 'SAMEORIGIN'
```

### **5. Reiniciar serviços:**
```bash
sudo systemctl restart uwsgi
sudo systemctl restart nginx
```

### **6. Testar:**
```bash
curl -I https://gserp.com.br
```

## 🆘 **SE AINDA NÃO FUNCIONAR - SOLUÇÃO DE EMERGÊNCIA:**

### **Opção 1: Comentar o middleware problemático**
```bash
cd /var/www/New-Goldensat
cp int/settings.py int/settings.py.backup
```

Editar o arquivo `int/settings.py` e encontrar a seção `MIDDLEWARE`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',  # COMENTADO
]
```

### **Opção 2: Forçar configuração no .env**
```bash
cd /var/www/New-Goldensat
cat >> .env << EOF
X_FRAME_OPTIONS=SAMEORIGIN
EOF
```

## 🎯 **COMANDOS COMPLETOS EM SEQUÊNCIA:**

```bash
# 1. Corrigir Git
cd /var/www/New-Goldensat
git config --global --add safe.directory /var/www/New-Goldensat

# 2. Fazer pull
git pull origin main

# 3. Verificar arquivo
grep -n "X_FRAME_OPTIONS" int/settings.py

# 4. Se necessário, corrigir manualmente
sed -i "s/X_FRAME_OPTIONS = None/X_FRAME_OPTIONS = 'SAMEORIGIN'/g" int/settings.py

# 5. Reiniciar
sudo systemctl restart uwsgi
sudo systemctl restart nginx

# 6. Testar
curl -I https://gserp.com.br
```

**Execute esses comandos em ordem!**
