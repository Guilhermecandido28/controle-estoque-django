# rabbitmq_publisher.py
import pika
import json
from django.conf import settings
from typing import Dict

class RabbitMQPublisher:
    def __init__(self) -> None:
        self.__host = settings.RABBITMQ_HOST
        self.__port = settings.RABBITMQ_PORT
        self.__username = settings.RABBITMQ_USERNAME
        self.__password = settings.RABBITMQ_PASSWORD
        self.__exchange = settings.RABBITMQ_EXCHANGE
        self.__routing_key = settings.RABBITMQ_ROUTING_KEY
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(self.__username, self.__password),
        )

        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        return channel

    def send_message(self, body: Dict):
        try:
            # Converte o dicionário para JSON e depois para bytes
            
            
            self.__channel.basic_publish(
                exchange=self.__exchange,
                routing_key=self.__routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2  # Persistência da mensagem
                )
            )
        
        # Fecha a conexão após enviar a mensagem
            self.__channel.close()
        except Exception as e:
            print(f"Erro ao enviar mensagem para o RabbitMQ: {e}")
