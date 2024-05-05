# Changelog

All notable changes to this project will be documented in this file.

## [1.5.0] - 2024-05-05

### Bug Fixes

- New spreaker urlparse + update deps

### Documentation

- Adding screenshot + contributing and code of conduct

### Miscellaneous Tasks

- Bump psycopg[binary] + bump django-filter
- Bump actions/setup-python from 4 to 5
- Bump alpine from 3.18 to 3.19
- Bump feedparser from 6.0.10 to 6.0.11
- Bump pre-commit from 3.5.0 to 3.6.0
- Bump drf-spectacular from 0.26.5 to 0.27.0
- Bump black from 23.11.0 to 23.12.0
- Bump github/codeql-action from 2 to 3
- Bump django-allauth from 0.58.2 to 0.59.0
- Bump actions/download-artifact from 3 to 4
- Bump actions/upload-artifact from 3 to 4
- Bump psycopg[binary] from 3.1.14 to 3.1.15
- Bump coverage from 7.3.2 to 7.3.3
- Bump hiredis from 2.2.3 to 2.3.2
- Bump psycopg[binary] from 3.1.15 to 3.1.16
- Bump djlint from 1.34.0 to 1.34.1
- Bump coverage from 7.3.3 to 7.3.4
- Bump black from 23.12.0 to 23.12.1
- Bump coverage from 7.3.4 to 7.4.0
- Bump pytest from 7.4.3 to 7.4.4
- Bump yt-dlp from 2023.11.16 to 2023.12.30
- Bump psycopg[binary] from 3.1.16 to 3.1.17
- Bump flake8 from 6.1.0 to 7.0.0
- Bump django-allauth from 0.59.0 to 0.60.0
- Bump django-allauth from 0.60.0 to 0.60.1
- Bump beautifulsoup4 from 4.12.2 to 4.12.3
- Bump drf-spectacular from 0.27.0 to 0.27.1
- Bump python-slugify from 8.0.1 to 8.0.2
- Bump pillow from 10.1.0 to 10.2.0
- Bump coverage from 7.4.0 to 7.4.1
- Bump pytest from 7.4.4 to 8.0.0
- Bump black from 23.12.1 to 24.1.1
- Bump pytest-sugar from 0.9.7 to 1.0.0
- Bump python-slugify from 8.0.2 to 8.0.3
- Bump psycopg[binary] from 3.1.17 to 3.1.18
- Bump django-debug-toolbar from 4.2.0 to 4.3.0
- Bump pytest-django from 4.7.0 to 4.8.0
- Bump pre-commit/action from 3.0.0 to 3.0.1
- Bump django-allauth from 0.60.1 to 0.61.0
- Bump python-slugify from 8.0.3 to 8.0.4
- Bump pre-commit from 3.6.0 to 3.6.1
- Bump django-model-utils from 4.3.1 to 4.4.0
- Bump django-allauth from 0.61.0 to 0.61.1
- Bump pytest from 8.0.0 to 8.0.1
- Bump pre-commit from 3.6.1 to 3.6.2
- Bump black from 24.1.1 to 24.2.0
- Bump orhun/git-cliff-action from 2 to 3
- Bump coverage from 7.4.1 to 7.4.2
- Bump crispy-bootstrap5 from 2023.10 to 2024.2
- Bump coverage from 7.4.2 to 7.4.3
- Bump pytest from 8.0.1 to 8.0.2
- Bump django-celery-beat from 2.5.0 to 2.6.0
- Bump softprops/action-gh-release from 1 to 2
- Bump pytest from 8.0.2 to 8.1.1
- Bump redis from 5.0.1 to 5.0.3
- Bump django from 4.2.7 to 5.0.3
- Bump coverage from 7.4.3 to 7.4.4
- Bump django-filter from 23.5 to 24.1
- Bump black from 24.2.0 to 24.3.0
- Bump djangorestframework from 3.14.0 to 3.15.0
- Bump yt-dlp from 2023.12.30 to 2024.3.10
- Bump pre-commit from 3.6.2 to 3.7.0
- Bump pillow from 10.2.0 to 10.3.0
- Bump django-model-utils from 4.4.0 to 4.5.0
- Bump django-filter from 24.1 to 24.2
- Update docker image + Adding init container
- Bump drf-spectacular from 0.27.1 to 0.27.2
- Bump django from 5.0.3 to 5.0.4
- Bump werkzeug[watchdog] from 3.0.1 to 3.0.2
- Bump djangorestframework from 3.15.0 to 3.15.1


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.4.0] - 2023-12-02

### Bug Fixes

- Force settings name to be unique
- Fix mobile responsive design
- _after_postgeneration warning (https://github.com/cookiecutter/cookiecutter-django/pull/4534)
- Fix reference select_audio + Fix next audio break stop loop

### Features

- Adding Action/Task API
- Adding Tasks/Action run on settings page (via API)
- Adding resume function on player

### Miscellaneous Tasks

- Bump django-filter from 23.3 to 23.4
- Bump celery from 5.3.5 to 5.3.6

### Testing

- Adding models check


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.3.0] - 2023-11-20

### Bug Fixes

- Fix static player img
- Adding user auth filter on navbar + Adjust login page
- Restyle playlist list on player page

### Documentation

- Adding docs about helm + Adding new venv

### Features

- Rework the cache layer for the pages

### Miscellaneous Tasks

- Bump psycopg[binary] from 3.1.12 to 3.1.13


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.9] - 2023-11-19

### Bug Fixes

- Export CSRF_TRUSTED_ORIGINS venv


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.8] - 2023-11-19

### Bug Fixes

- Adding DJANGO_ALLOWED_HOSTS venv + Adding DEBUG_INTERNALIPS venv


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.7] - 2023-11-19

### Miscellaneous Tasks

- Fix changelog generator


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.6] - 2023-11-18

### Miscellaneous Tasks

- Fix changelog generator


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.5] - 2023-11-18

### Miscellaneous Tasks

- Adding dockerinfo on GH


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.4] - 2023-11-18

### Miscellaneous Tasks

- Adding path ignore + Add changelog on develop


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.3] - 2023-11-18

### Miscellaneous Tasks

- Fix commit msg / user


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.2] - 2023-11-18

### Miscellaneous Tasks

- Fix docker platform + remove typ


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.1] - 2023-11-18

### Miscellaneous Tasks

- Add docker labels + Fix docker security issues + Add full changelog


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.2.0] - 2023-11-16

### Features

- Adding simple health check page

### Miscellaneous Tasks

- Adding OpenContainers Labels to dockerfile
- Upgrade yt-dlp deps
- Adding dependabot settings for standard commit msg


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.1.2] - 2023-11-15

### Miscellaneous Tasks

- Limit changelog generation only for tags
- Fix dockerfile reference for git-cliff

### Refactor

- Update Celery,django-cors-headers,yt-dlp


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.1.1] - 2023-11-15

### Miscellaneous Tasks

- Adding changelog in the release page


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

## [1.1.0] - 2023-11-15

### Features

- Adding Playlist page + Switch Dockerfile to userspace

### Miscellaneous Tasks

- Adding Git-cliff integration


Docker package: [https://github.com/Mirio/verbacap/pkgs/container/verbacap](https://github.com/Mirio/verbacap/pkgs/container/verbacap)

<!-- generated by git-cliff -->
