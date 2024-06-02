from producer_interface import mqProducerInterface
import os
import pika


# - setupRMQConnection Function: Establish connection to the RabbitMQ service.
# - publishOrder:  Publish a simple UTF-8 string message from the parameter.
# - publishOrder:  Close Channel and Connection.  
class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str):
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        self.channel = self.connection.channel()
        self.exchange = self.channel.exchange_declare(exchange=self.exchange_name)
    
    def publishOrder(self, message: str) -> None:
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
        )
        self.channel.close()
        self.connection.close()