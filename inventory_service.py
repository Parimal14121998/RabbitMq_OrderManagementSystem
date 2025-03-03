import pika
import json


def update_inventory():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a direct exchange and bind the queue to the exchange
    channel.exchange_declare(exchange='order_exchange', exchange_type='direct')
    channel.queue_declare(queue='order_queue', durable=True)
    channel.queue_bind(queue='order_queue', exchange='order_exchange', routing_key='payment.success')

    def callback(ch, method, properties, body):
        order_data = json.loads(body)
        print(f"Updating inventory for Order: {order_data}")

        # Simulate inventory update logic
        inventory_updated = True  # Simulate inventory update success

        if inventory_updated:
            print("Inventory updated successfully!")
            # After updating inventory, publish a success message for email
            channel.basic_publish(
                exchange='order_exchange',
                routing_key='inventory.updated',  # Routing key for email service
                body=json.dumps(order_data)
            )
            print("Inventory update message sent to RabbitMQ!")

        ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

    # Consume messages from the queue
    channel.basic_consume(queue='order_queue', on_message_callback=callback)

    print('Waiting for payment success messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    update_inventory()
