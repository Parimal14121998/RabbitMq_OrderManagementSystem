from flask import Flask
from flask_restx import Api, Resource, fields
import pika
import json

# Create the Flask app and the Flask-RESTX API instance
app = Flask(__name__)
api = Api(app)

# Define the Order API model (request validation)
order_model = api.model('Order', {
    'product_id': fields.Integer(required=True, description='The product ID'),
    'quantity': fields.Integer(required=True, description='Quantity of the product'),
    'user_id': fields.Integer(required=True, description='ID of the user placing the order')
})

class OrderService(Resource):
    @api.expect(order_model)
    def post(self):
        # Extract order data from the request
        order_data = api.payload
        product_id = order_data['product_id']
        quantity = order_data['quantity']
        user_id = order_data['user_id']

        # Simulate placing the order in the database (this would be a real DB call)
        print(f"Order placed: Product ID {product_id}, Quantity {quantity}, User ID {user_id}")

        # Send message to RabbitMQ (Order created)
        self.send_message_to_queue(order_data)

        return {'message': 'Order placed successfully!', 'order': order_data}, 201

    def send_message_to_queue(self, order_data):
        # RabbitMQ connection
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        # Declare a direct exchange
        channel.exchange_declare(exchange='order_exchange', exchange_type='direct')

        # Declare a queue for the order
        channel.queue_declare(queue='order_queue', durable=True)

        # Send the order message to the queue
        channel.basic_publish(
            exchange='order_exchange',
            routing_key='order.created',  # Routing key used by consumers
            body=json.dumps(order_data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        )

        print("Order message sent to RabbitMQ!")
        connection.close()

# Add the order service route to the API
api.add_resource(OrderService, '/api/orders')

if __name__ == '__main__':
    app.run(debug=True)
