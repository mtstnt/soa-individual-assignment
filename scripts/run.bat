set /A isFromScriptsDir = 0
if %cd:\scripts% == %cd% set /A isFromScriptsDir = 1

if %isFromScriptsDir% == 1 (
	cd ..
)

echo "Starting Redis server using Docker..."
start docker run --rm -d --name redis-server -p 6379:6379 redis:alpine3.15

echo "Starting user service..."
cd user_service && start pipenv run nameko run main
cd ..

echo "Starting calculation service..."
cd calculation_service && start pipenv run nameko run main
cd ..

echo "Starting user service..."
cd user_service && start pipenv run nameko run user
cd ..

echo "All services started successfully."