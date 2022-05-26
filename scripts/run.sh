# !/usr/bin/sh

# Start redis
# docker run --rm -d --name redis-server -p 6379:6379 redis:alpine3.15

# Start user service
cd user_service
nameko run user &

cd ..

# Start calculation service
cd calculation_service
nameko run calculation &

cd ..

# Start gateway service
cd gateway_service
nameko run gateway &

cd ..