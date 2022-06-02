# !/usr/bin/sh

echo "Checking if docker is OK."
if (( $? >= 1 )); then
	echo "Docker is not OK. Exiting..."
	exit 1
fi

launched_pids=()

# Start redis
echo "Running Redis Server on port 6379"
docker run --rm -d --name redis-server -p 6379:6379 redis:alpine3.15

echo "Running RabbitMQ Server on port 5672"
docker run --rm -d --name rabbitmq-server -p 5672:5672 rabbitmq:3.9.17-alpine

# Start user service
echo "Starting services in background: "
echo "User Service..."
cd user_service
nameko run main &
launched_pids+=($!)

cd ..

# Start calculation service
echo "Calculation Service..."
cd calculation_service
nameko run main &
launched_pids+=($!)

cd ..

# Start gateway service
echo "Gateway Service..."
cd gateway_service
nameko run main &
launched_pids+=($!)

cd ..

read -p "Press Enter to stop session..."

for i in "${launched_pids[@]}"; do
	pkill $i
done

docker container stop rabbitmq-server redis-server