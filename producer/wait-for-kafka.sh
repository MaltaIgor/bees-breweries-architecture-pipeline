#!/bin/bash
KAFKA_HOST=${KAFKA_BROKER:-kafka:9092}

echo "Aguardando Kafka em $KAFKA_HOST..."
while ! nc -z $(echo $KAFKA_HOST | cut -d: -f1) $(echo $KAFKA_HOST | cut -d: -f2); do
  sleep 1
done

echo "Kafka está online. Iniciando produtor..."
exec python produce.py


