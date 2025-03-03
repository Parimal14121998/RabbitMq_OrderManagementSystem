import pika
import json


def send_confirmation_email():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a direct exchange and bind the queue to the exchange
    channel.exchange_declare(exchange='order_exchange', exchange_type='direct')
    channel.queue_declare(queue='order_queue', durable=True)
    channel.queue_bind(queue='order_queue', exchange='order_exchange', routing_key='inventory.updated')

    def callback(ch, method, properties, body):
        order_data = json.loads(body)
        print(f"Sending confirmation email for Order: {order_data}")

        # Simulate email sending logic
        email_sent = True  # Simulate email sent

        if email_sent:
            print("Confirmation email sent successfully!")

        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

    # Consume messages from the queue
    channel.basic_consume(queue='order_queue', on_message_callback=callback)

    print('Waiting for inventory update messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    send_confirmation_email()
