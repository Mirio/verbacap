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
[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/verbacap)](https://artifacthub.io/packages/helm/verbacap/verbacap)



With VerbaCap is a **Podcast Manager** you will be able to download and listen to all of your favorite podcasts in a centralized way.

It uses [_Django_](https://www.djangoproject.com/) in order to create a new integration for the platform as easy as possible. Below a quick platform integrated and the current status.

:heavy_check_mark: Youtube Channel :heavy_check_mark: Youtube Playlist

:heavy_check_mark: Spreaker.com

:construction: Apple Podcast :construction: Amazon Music

[Installation](docs/install.md) • [Configuration](docs/config.md)

</div>

## Features
* Download from Youtube
* Download from Youtube Playlists
* Download from Spreaker.com
* Pulls every day the list of episode from all datasources
* Player with automatic resume
* Auto-removal of listened episodes
* No distraction Audio Player
* Volume button for the quick adjust on the mobile devices
* Fully Containerized
* Lightweight

## Screenshot

<p align="center">
    Homepage
    <img src="https://raw.githubusercontent.com/Mirio/verbacap/main/docs/assets/dashboard_desktop.png"
    alt="Dashboard Desktop"
    width="1024">
</p>

<p align="center">
    Episode Details
    <img src="https://raw.githubusercontent.com/Mirio/verbacap/main/docs/assets/episodes_desktop.png"
    alt="Episodes Desktop"
    width="1024">
</p>

<p align="center">
    Player
    <img src="https://raw.githubusercontent.com/Mirio/verbacap/main/docs/assets/player_desktop.png"
    alt="Player Desktop"
    width="1024">
</p>

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

## 🤝 Contributing
Contributions, issues and feature requests are welcome.<br />
Feel free to check [issues page](https://github.com/Mirio/verbacap/issues) if you want to contribute.<br />
[Check the contributing guide](./CONTRIBUTING.md).<br />

## 📝 License
Copyright © [Mirio](https://github.com/Mirio).<br />
This project is [MIT](https://github.com/Mirio/verbacap/blob/main/README.md) licensed.
