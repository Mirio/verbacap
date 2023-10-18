<div align="center">

# VerbaCap

[![CodeQL](https://github.com/Mirio/verbacap/actions/workflows/codeql-action.yml/badge.svg)](https://github.com/Mirio/verbacap/actions/workflows/codeql-action.yml)
[![CodeCov](https://codecov.io/gh/Mirio/verbacap/branch/main/graph/badge.svg?token=KOIGVN4J99)](https://codecov.io/gh/Mirio/verbacap)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Mirio_verbacap&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Mirio_verbacap)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Mirio_verbacap&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=Mirio_verbacap)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Mirio_verbacap&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=Mirio_verbacap)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=Mirio_verbacap&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=Mirio_verbacap)

![GitHub](https://img.shields.io/github/license/mirio/verbacap)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)




With VerbaCap is a **Podcast Manager** you will be able to download and listen to all of your favorite podcasts in a centralized way.

It uses [_Django_](https://www.djangoproject.com/) in order to create a new integration for the platform as easy as possible. Below a quick platform integrated and the current status.

:heavy_check_mark: Youtube Channel :heavy_check_mark: Youtube Playlist

:heavy_check_mark: Spreaker.com

:construction: Apple Podcast :construction: Amazon Music

[Installation](docs/install.md) • [Configuration](docs/config.md)

</div>

## Quick Demo
Below all the information to start a quick demo locally using Docker, for more stable solution please follow the [Installation](docs/install.md) guide.

1. Install `docker` and `docker-compose` ([More Info](https://docs.docker.com/engine/install/))
2. Run the command below to start the containers
```
docker compose -f compose-demo.yaml up -d
```
3. Wait until the container is ready
```
docker logs -f verbacap-web
```
Wait until you can see `Listening at: http://0.0.0.0:8000`

4. Create a superadmin user using:
```
docker exec -it verbacap-web /entrypoint.bash createadminuser
```
Insert the user and password of the superadmin

5. Open your browser to [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

6. Login with the superadmin credential

7. Go to Episode -> Add Datasource -> Add Youtube Channel and insert

**Channel Name**: Youtube Official

**Channel URL**: https://www.youtube.com/@youtube

-> Submit

8. Wait a few minute to scrape the page based by your internet connection

9. Go to "Episode" Page -> Click on "Add to Playlist"

10. Go to Player and listen it
