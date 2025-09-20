# 🚨 ERRO 500 - DEBUG URGENTE

## 🔍 **DIAGNÓSTICO DO ERRO 500:**

### **1. Verificar logs do uWSGI:**
```bash
sudo tail -f /var/log/uwsgi/app/gserp.log
```

### **2. Verificar logs do Nginx:**
```bash
sudo tail -f /var/log/nginx/error.log
```

### **3. Verificar logs do Django:**
```bash
tail -f /var/www/New-Goldensat/logs/django.log
```

### **4. Testar Django diretamente:**
```bash
cd /var/www/New-Goldensat
source venv/bin/activate
python manage.py check --deploy
```

## 🛠️ **CORREÇÕES POSSÍVEIS:**

### **1. Problema com arquivo .env:**
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

### **2. Problema com permissões:**
```bash
sudo chown -R www-data:www-data /var/www/New-Goldensat/
sudo chmod -R 755 /var/www/New-Goldensat/
```

### **3. Problema com banco de dados:**
```bash
cd /var/www/New-Goldensat
source venv/bin/activate
python manage.py migrate
```

### **4. Problema com arquivos estáticos:**
```bash
cd /var/www/New-Goldensat
source venv/bin/activate
python manage.py collectstatic --noinput
```

### **5. Verificar se o socket existe:**
```bash
ls -la /var/www/New-Goldensat/gserp.sock
```

Se não existir, recriar:
```bash
sudo systemctl restart uwsgi
```

## 🔧 **CONFIGURAÇÃO TEMPORÁRIA PARA DEBUG:**

Se precisar ativar DEBUG temporariamente para ver o erro:

```bash
cd /var/www/New-Goldensat
cat > .env << EOF
DEBUG=True
SECRET_KEY=django-insecure-7=sd^vwv+in5&os2t1zv00*#n#hr85rssdgj7b6kv%g36s#p@^
ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br,127.0.0.1
EOF

sudo systemctl restart uwsgi
```

**ATENÇÃO:** Lembre-se de voltar DEBUG=False depois!

## 📋 **CHECKLIST DE VERIFICAÇÃO:**

- [ ] Arquivo .env existe e está correto
- [ ] Permissões dos arquivos estão corretas
- [ ] Banco de dados está migrado
- [ ] Arquivos estáticos foram coletados
- [ ] Socket do uWSGI existe
- [ ] Serviços estão rodando
- [ ] Logs não mostram erros críticos

## 🆘 **SE NADA FUNCIONAR:**

1. **Verificar se o Python está funcionando:**
```bash
cd /var/www/New-Goldensat
source venv/bin/activate
python -c "import django; print(django.get_version())"
```

2. **Verificar se o Django está funcionando:**
```bash
python manage.py shell
```

3. **Verificar se o banco está acessível:**
```bash
python manage.py dbshell
```
