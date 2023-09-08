#!/bin/bash

ACTION="${1}"

function help() {
    echo -e "Entrypoint for VerbaCap\nArguments:\n"
    echo -e "\tdebugrun\tStart the app in debug mode"
    echo -e "\tcelery\t\tStart Celery with Beat included"
    echo -e "\tpyshell\t\tStart an interative Django shell"
    echo -e "\trun\t\tStart the app"
    echo -e "\tshell\t\tInteractive Shell /bin/bash with all vars loaded"
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

# Load virtualenv
cd "${HOME}"
. "${HOME}/venv/bin/activate"

# Actions
case "${ACTION}" in
    debugrun)
        echo "Staring App with debug"
        export DJANGO_DEBUG="True"
        python3 manage.py runserver 8080
        ;;
    celery)
        echo "Starting Celery"
        celery -A config.celery_app worker --loglevel="info" -c 1 -B
        ;;
    pyshell)
        echo "Starting Django interactive shell"
        python3 manage.py shell
        ;;
    run)
        echo "Starting App"
        gunicorn config.wsgi --bind 0.0.0.0:8080
        ;;
    shell)
        echo "Staring Interactive Bash shell"
        /bin/bash
        ;;
    *)
        help
        ;;
esac
