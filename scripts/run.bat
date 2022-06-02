@echo off
echo Running `docker images` to check if docker is OK...
echo:
docker images

if %ERRORLEVEL% GEQ 1 ( 
	echo Error initializing docker!
	exit /B
)

echo Starting Redis server using Docker...
echo:

start docker run --rm -d --name redis-server -p 6379:6379 redis:alpine3.15

echo Starting RabbitMQ Server using Docker...
echo:

start docker run --rm -d --name rabbitmq-server -p 5672:5672 rabbitmq:3.9.17-alpine

echo Starting user service...
echo:

cd user_service && start pipenv run nameko run main
cd ..

echo Starting calculation service...
echo:
cd calculation_service && start pipenv run nameko run main
cd ..

echo Starting user service...
echo:
cd gateway_service && start pipenv run nameko run main
cd ..

echo All services started. Please check any errors in their CMD windows.
echo:

set /p stopAll=To end session, close all Nameko CMD windows and press Enter.

echo Stopping docker containers...
echo:

docker container stop redis-server rabbitmq-server