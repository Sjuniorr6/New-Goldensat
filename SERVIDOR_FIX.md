# 🔧 CORREÇÃO NO SERVIDOR - Golden SAT

## 🚨 **PROBLEMA IDENTIFICADO:**

O Nginx está configurado para servir mídia de:
```nginx
location /media/ { alias /var/www/New-Goldensat/media/; }
```

Mas o Django estava configurado para:
```python
MEDIA_ROOT = BASE_DIR.parent / 'media'   # /var/www/media
```

## ✅ **SOLUÇÃO APLICADA:**

Corrigi o `settings.py` para:
```python
MEDIA_ROOT = BASE_DIR / 'media'   # /var/www/New-Goldensat/media
```

## 🚀 **COMANDOS PARA EXECUTAR NO SERVIDOR:**

```bash
# 1. Fazer pull das alterações
cd /var/www/New-Goldensat
git pull origin main

# 2. Reiniciar serviços
sudo systemctl restart nginx
sudo systemctl restart uwsgi

# 3. Verificar se os arquivos de mídia existem
ls -la /var/www/New-Goldensat/media/

# 4. Se não existir, criar o diretório
mkdir -p /var/www/New-Goldensat/media

# 5. Copiar arquivos de mídia se necessário
# (se os arquivos estão em outro local)
```

## 📁 **ESTRUTURA CORRETA NO SERVIDOR:**

```
/var/www/
├── New-Goldensat/          # Projeto Django
│   ├── int/
│   ├── media/              # ✅ Arquivos de mídia aqui
│   │   ├── usuarios/
│   │   └── imagens/
│   └── manage.py
└── staticfiles/            # ✅ Arquivos estáticos coletados
```

## 🔍 **VERIFICAÇÕES:**

1. **Verificar se o diretório media existe:**
   ```bash
   ls -la /var/www/New-Goldensat/media/
   ```

2. **Verificar permissões:**
   ```bash
   sudo chown -R www-data:www-data /var/www/New-Goldensat/media/
   sudo chmod -R 755 /var/www/New-Goldensat/media/
   ```

3. **Testar o site:**
   - Acessar: https://gserp.com.br
   - Verificar se CSS/JS carregam
   - Verificar se imagens carregam

## ⚠️ **SE AINDA NÃO FUNCIONAR:**

1. **Verificar logs do Nginx:**
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

2. **Verificar logs do uWSGI:**
   ```bash
   sudo tail -f /var/log/uwsgi/app/gserp.log
   ```

3. **Verificar se o arquivo .env existe:**
   ```bash
   ls -la /var/www/New-Goldensat/.env
   ```

4. **Criar arquivo .env se não existir:**
   ```bash
   cd /var/www/New-Goldensat
   echo "DEBUG=False" > .env
   echo "SECRET_KEY=sua-chave-secreta-aqui" >> .env
   echo "ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br" >> .env
   ```
