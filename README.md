container for api (fastapi)
container for db (postgresql)

rename .env.example to .env

make sure port 8000 isn't used

needs docker compose to be properly installed on machine

to build and run console attached : docker compose up

to build and run console deattached (in background) : docker compose up -d

to build new container if there any changes in project: docker-compose up --build --force-recreate

to shutdown: docker compose down

to shutdown and WIPE ALL DATA : docker compose down -v

api docks link : http://0.0.0.0:8000/docs#/
