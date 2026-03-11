#!/usr/bin/env bash
set -euo pipefail

# ────────────────────────────────────────────────
#          Настройки — меняй только здесь если нужно
# ────────────────────────────────────────────────

PROJECT_NAME="Linka-backend"
PROJECT_ROOT="/var/www/${PROJECT_NAME}"
DOMAIN_OR_IP="164.90.219.190"           # ← твой IP или домен

VENV_PATH="${PROJECT_ROOT}/venv"
GUNICORN_SOCK="${PROJECT_ROOT}/${PROJECT_NAME}.sock"
SERVICE_NAME="${PROJECT_NAME}.service"
NGINX_CONF="/etc/nginx/sites-available/${PROJECT_NAME}.conf"

# ────────────────────────────────────────────────

echo "→ Deploy ${PROJECT_NAME} (SQLite mode)"

# 1. Установка зависимостей системы
apt-get update -qq
apt-get install -y -qq nginx python3.13 python3.13-venv python3.13-dev

# 2. Активируем виртуальное окружение (оно уже есть)
source "${VENV_PATH}/bin/activate" || { echo "venv не найден или сломан"; exit 1; }

# 3. Обновляем pip и ставим/обновляем зависимости
echo "→ Установка/обновление пакетов из requirements.txt"
pip install --quiet --upgrade pip setuptools wheel
pip install --quiet -r requirements.txt
pip install --quiet gunicorn               # на всякий случай

# 4. Django-команды
echo "→ collectstatic + migrate"
python manage.py collectstatic --noinput || true
python manage.py migrate --noinput

# 5. Создаём/пересоздаём systemd-сервис
echo "→ Создаём systemd сервис: ${SERVICE_NAME}"

cat > "/etc/systemd/system/${SERVICE_NAME}" <<EOF
[Unit]
Description=Gunicorn для ${PROJECT_NAME}
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=${PROJECT_ROOT}
Environment="PATH=${VENV_PATH}/bin"
ExecStart=${VENV_PATH}/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:${GUNICORN_SOCK} \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# 6. Перечитываем и (пере)запускаем сервис
systemctl daemon-reload
systemctl enable --now "${PROJECT_NAME}" || {
    systemctl restart "${PROJECT_NAME}"
}

# 7. Nginx конфигурация
echo "→ Создаём конфиг nginx: ${NGINX_CONF}"

cat > "${NGINX_CONF}" <<EOF
server {
    listen 80;
    server_name ${DOMAIN_OR_IP};

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias ${PROJECT_ROOT}/static/;
    }

    location /staticfiles/ {
        alias ${PROJECT_ROOT}/staticfiles/;
    }

    location /media/ {
        alias ${PROJECT_ROOT}/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:${GUNICORN_SOCK};
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# 8. Активируем конфиг nginx
rm -f /etc/nginx/sites-enabled/default
ln -sf "${NGINX_CONF}" /etc/nginx/sites-enabled/ 2>/dev/null || true

# 9. Проверка и перезапуск nginx
nginx -t && systemctl reload nginx || {
    echo "!!! Ошибка в конфиге nginx !!!"
    cat "${NGINX_CONF}"
    echo ""
    nginx -t
    exit 1
}

echo ""
echo "====================================="
echo "  Деплой завершён (проверь статус)"
echo "====================================="
echo "systemctl status ${PROJECT_NAME}"
echo "sudo tail -n 30 /var/log/nginx/error.log"
echo "curl -I http://${DOMAIN_OR_IP}"
echo "→ Всё должно работать через http://${DOMAIN_OR_IP}"
