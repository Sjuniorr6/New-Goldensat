# 🚨 SOLUÇÃO DIRETA PARA ERRO 500

## 🔥 **PROBLEMA:**
O servidor ainda está com a configuração antiga que causa o erro:
```
AttributeError: 'NoneType' object has no attribute 'upper'
```

## ✅ **SOLUÇÃO IMEDIATA:**

### **1. Verificar se o git pull foi executado:**
```bash
cd /var/www/New-Goldensat
git status
git log --oneline -5
```

### **2. Se não foi feito pull, executar:**
```bash
cd /var/www/New-Goldensat
git pull origin main
```

### **3. Verificar se o arquivo foi atualizado:**
```bash
grep -n "X_FRAME_OPTIONS" int/settings.py
```

Deve mostrar:
```
167:X_FRAME_OPTIONS = 'SAMEORIGIN'  # Corrigido - não pode ser None
```

### **4. Se ainda estiver com None, corrigir manualmente:**
```bash
cd /var/www/New-Goldensat
sed -i "s/X_FRAME_OPTIONS = None/X_FRAME_OPTIONS = 'SAMEORIGIN'/g" int/settings.py
sed -i "s/CSRF_COOKIE_SAMESITE = None/CSRF_COOKIE_SAMESITE = 'Lax'/g" int/settings.py
sed -i "s/SESSION_COOKIE_SAMESITE = None/SESSION_COOKIE_SAMESITE = 'Lax'/g" int/settings.py
```

### **5. Reiniciar serviços:**
```bash
sudo systemctl restart uwsgi
sudo systemctl restart nginx
```

### **6. Verificar se funcionou:**
```bash
curl -I https://gserp.com.br
```

## 🆘 **SE AINDA NÃO FUNCIONAR:**

### **Opção 1: Remover o middleware temporariamente**
```bash
cd /var/www/New-Goldensat
cp int/settings.py int/settings.py.backup
```

Editar o arquivo `int/settings.py` e comentar a linha:
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

## 🎯 **VERIFICAÇÃO FINAL:**
```bash
# Verificar se o site está funcionando
curl -s https://gserp.com.br | head -20

# Verificar logs
sudo tail -f /var/log/uwsgi/app/gserp.log
```

**Execute essas etapas em ordem até o site funcionar!**
