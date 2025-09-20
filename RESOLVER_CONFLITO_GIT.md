# 🔧 RESOLVER CONFLITO DO GIT

## 🚨 **PROBLEMA:**
```
error: Your local changes to the following files would be overwritten by merge:
        int/settings.py
Please commit your changes or stash them before you merge.
```

## ✅ **SOLUÇÃO - Execute no servidor:**

### **Opção 1: Fazer stash das alterações locais (RECOMENDADO)**
```bash
cd /var/www/New-Goldensat
git stash
git pull origin main
```

### **Opção 2: Descartar alterações locais e fazer pull**
```bash
cd /var/www/New-Goldensat
git checkout -- int/settings.py
git pull origin main
```

### **Opção 3: Fazer commit das alterações locais primeiro**
```bash
cd /var/www/New-Goldensat
git add int/settings.py
git commit -m "Correção local do settings.py"
git pull origin main
```

## 🎯 **RECOMENDO A OPÇÃO 1 (stash):**

```bash
cd /var/www/New-Goldensat
git stash
git pull origin main
```

## 🚀 **Depois do pull, reiniciar serviços:**

```bash
sudo systemctl restart uwsgi
sudo systemctl restart nginx
```

## 🔍 **Verificar se funcionou:**

```bash
curl -I https://gserp.com.br
```

**Execute a Opção 1 (git stash) que é a mais segura!**
