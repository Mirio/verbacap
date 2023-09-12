#!/bin/bash

ACTION="${1}"

function help() {
    echo -e "Entrypoint for VerbaCap\nArguments:\n"
    echo -e "\tcreateadminuser\t\tCreate superuser account"
    echo -e "\tcelery\t\tStart Celery with Beat included"
    echo -e "\tdebugrun\tStart the app in debug mode"
    echo -e "\tpyshell\t\tStart an interative Django shell"
    echo -e "\trun\t\tStart the app"
    echo -e "\tshell\t\tInteractive Shell /bin/bash with all vars loaded"
}

function prepare() {
    echo "-- Collect Static"
    python3 manage.py collectstatic --no-input --clear
    echo "-- Migrate DB"
    python3 manage.py migrate
    echo "-- Generate compress files"
    python3 manage.py compress
    echo "-- Load Fixtures"
    python3 manage.py loaddata "fixtures/main.json"
}

# Precheck validation
if [[ ! -v DATABASE_URL ]]; then
    echo "CRIICAL Please set DATABASE_URL var!"
    exit 1
fi
if [[ ! -v DJANGO_SECRET_KEY ]]; then
    echo "CRIICAL Please set DJANGO_SECRET_KEY var!"
    exit 1
fi
if [[ ! -v CELERY_BROKER_URL ]]; then
    echo "CRIICAL Please set CELERY_BROKER_URL var!"
    exit 1
fi
if [[ ! -v PERSIST_AUDIO_ROOTDIR ]]; then
    echo "CRIICAL Please set PERSIST_AUDIO_ROOTDIR var!"
    exit 1
fi

echo "Waiting for DB ready"
DB_ADDR=$(echo "$DATABASE_URL" |cut -d'@' -f2|cut -d':' -f1)
while ! nc -z "${DB_ADDR}" 5432; do
    echo "DB '${DB_ADDR}' not ready..."
    sleep 1
done
echo "Database Ready."

# Chown Fix
sudo chown -R "app:app" "${PERSIST_AUDIO_ROOTDIR}"

# Load virtualenv
cd "${HOME}" || exit
# shellcheck disable=SC1091
. "${HOME}/venv/bin/activate"

# Actions
case "${ACTION}" in
    debugrun)
        echo "Staring App with debug"
        export DJANGO_DEBUG="True"
        prepare
        echo "--------"
        python3 manage.py runserver 8080
        ;;
    celery)
        echo "Starting Celery"
        echo "--------"
        # Waiting for first start for webapp
        sleep 60
        celery --app config.celery_app worker --loglevel="info" --concurrency 1 --beat
        ;;
    createadminuser)
        echo "Creating ADMIN user"
        echo "--------"
        python3 manage.py createsuperuser
        ;;
    pyshell)
        echo "Starting Django interactive shell"
        echo "--------"
        python3 manage.py shell
        ;;
    run)
        echo "Starting App"
        prepare
        echo "--------"
        sudo nginx
        gunicorn config.wsgi --bind 0.0.0.0:8000
        ;;
    shell)
        echo "Staring Interactive Bash shell"
        echo "--------"
        /bin/bash
        ;;
    *)
        help
        ;;
esac
