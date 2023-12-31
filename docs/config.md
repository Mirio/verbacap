## Environment Variables

| Variables | Default | Example | Description |
| :--------------------------: | :-----------------------: | :------------: |:--------------------------------------------: |
| DATABASE_URL | | postgres://user:password@localhost:5432/verbacap | Full Database URL |
| DJANGO_SECRET_KEY | | AAAaaaA51ag9A | A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value. |
| DJANGO_DEBUG | False | True | A boolean that turns on/off debug mode. |
| CELERY_BROKER_URL | | redis://verbacap-redis:6379/0 | Redis URL for store a celery data |
| PERSIST_AUDIO_ROOTDIR | /persist/audio | /persist/audio | Persist Path to store the audio files |
| DJANGO_ACCOUNT_ALLOW_REGISTRATION | False | False | A boolean that turns on/off the user registration. |
| DJANGO_ALLOWED_HOSTS | example.com | example.com | Django Allowed Hosts separated by comma |
| DEBUG_INTERNALIPS | 127.0.0.1 | 127.0.0.1,192.168.1.1 | If Debug is enabled, you can add your ip below to show the debug toolbar |
| CSRF_TRUSTED_ORIGINS | localhost,0.0.0.0,127.0.0.1 | 127.0.0.1 | CSRF_TRUSTED_ORIGINS exposed separated by comma |