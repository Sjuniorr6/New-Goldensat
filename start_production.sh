#!/bin/bash

# Script para iniciar o Golden SAT em produção

echo "Iniciando Golden SAT em produção..."

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Executar migrações
echo "Executando migrações..."
python manage.py migrate

# Iniciar uWSGI
echo "Iniciando uWSGI..."
uwsgi --ini goldensat_uwsgi.ini

echo "Golden SAT iniciado com sucesso!"
