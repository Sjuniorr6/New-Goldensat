# Configuração temporária para debug do erro 500
# Execute este comando no servidor para ativar DEBUG temporariamente

import os

# Criar arquivo .env com DEBUG=True temporariamente
env_content = """DEBUG=True
SECRET_KEY=django-insecure-7=sd^vwv+in5&os2t1zv00*#n#hr85rssdgj7b6kv%g36s#p@^
ALLOWED_HOSTS=gserp.com.br,www.gserp.com.br,127.0.0.1
"""

print("Execute estes comandos no servidor:")
print("=" * 50)
print("cd /var/www/New-Goldensat")
print("cat > .env << 'EOF'")
print(env_content.strip())
print("EOF")
print("sudo systemctl restart uwsgi")
print("=" * 50)
print("Depois acesse o site e veja o erro específico.")
print("LEMBRE-SE: Volte DEBUG=False depois!")
