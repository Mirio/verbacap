## Requirements
* Postgres 15+
* Docker / Podman / ContainerD
* HDD/SSD 2Gb +

## Install on Docker like daemon
1. Create a new user and assign full permission to the database in Postgres

2. Install `docker` and `docker-compose` ([More Info](https://docs.docker.com/engine/install/))

3. Edit the `compose.yaml` and change:
    * `POSTGRES_USERNAME` = Insert the username for PostGres
    * `POSTGRES_PASSWORD` = Insert the password for PostGres
    * `POSTGRES_HOSTNAME` = Insert the hostname for PostGres
    * `CHANGEME_PERSIST_PATH` = Insert the LOCAL path to persist the data like the audio files and temporary files
    * `CHANGEME_SECRET` = Generate a random secret for the hashing/salting functions

4. Start the containers
```
docker compose up -d
```

5. Wait until the container is ready
```
docker logs -f verbacap-web
```
Wait until you can see `Listening at: http://0.0.0.0:8000`

6. Create a super admin user using:
```
docker exec -it verbacap-web /entrypoint.bash createadminuser
```
Insert the user and password of the super admin

7. Open your browser to [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

8. Login with the super admin credential 
