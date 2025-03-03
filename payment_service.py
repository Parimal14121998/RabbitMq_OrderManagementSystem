import pika
import json


def process_payment():
    # Step 1: Establish connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Step 2: Declare a direct exchange and bind the queue to the exchange
    # Declaring an exchange named 'order_exchange' of type 'direct'
    channel.exchange_declare(exchange='order_exchange', exchange_type='direct')

    # Declaring a queue 'order_queue' to receive messages
    channel.queue_declare(queue='order_queue', durable=True)

    # Binding the 'order_queue' to the 'order_exchange' with the routing key 'order.created'
    channel.queue_bind(queue='order_queue', exchange='order_exchange', routing_key='order.created')

    # Step 3: Define a callback function to process incoming messages
    def callback(ch, method, properties, body):
        # Parse the message (which is in JSON format) into a Python dictionary
        order_data = json.loads(body)
        print(f"Processing payment for Order: {order_data}")

        # Simulate payment processing logic
        payment_success = True  # Simulate that payment is successful for this example

        if payment_success:
            # Payment has been processed successfully, so update the order status
            print("Payment processed successfully!")

            # Step 4: After processing payment, send a success message for the Inventory Service
            channel.basic_publish(
                exchange='order_exchange',  # Use the same exchange
                routing_key='payment.success',  # Routing key for inventory
                body=json.dumps(order_data),  # The body of the message contains the order data
            )
            print("Payment success message sent to RabbitMQ for Inventory Service!")
        else:
            # If payment fails, print a failure message
            print("Payment failed!")

        # Step 5: Acknowledge the message in the queue after processing
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Step 6: Start consuming messages from the 'order_queue'
    # The 'callback' function is called every time a new message is received
    channel.basic_consume(queue='order_queue', on_message_callback=callback)

    print('Waiting for order messages. To exit press CTRL+C')
    channel.start_consuming()


# Run the payment service
if __name__ == '__main__':
    process_payment()
