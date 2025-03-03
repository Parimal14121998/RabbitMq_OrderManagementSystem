# RabbitMq_OrderManagementSystem

# Project Overview
This project is a microservices-based order processing system built using Flask-RESTX and RabbitMQ. The system demonstrates the use of RabbitMQ as an event-driven messaging broker that allows multiple services (Payment Service, Inventory Service, and Email Service) to process the same order message in sequence. It ensures that the Payment, Inventory, and Email processes are handled in the correct order, with each service processing the message independently.

# Features
* Order Placement: An API endpoint that allows users to place an order.
* Payment Processing: The Payment Service processes the payment and sends the message to the next service (Inventory Service).
* Inventory Management: The Inventory Service updates the stock based on successful payment and notifies the next service (Email Service).
* Email Confirmation: The Email Service sends an email confirmation once inventory is updated.

# Technologies Used
* Python: Backend framework for building the API and services.
* Flask-RESTX: A simple and easy-to-use framework for building RESTful APIs.
* RabbitMQ: Message broker to facilitate communication between services using queues and exchanges.
* Pika: Python library for interacting with RabbitMQ.
* JSON: Data format used for communication between services.

# Project Structure
rabbitmq1.1/
├── app.py                  # Flask-RESTX app with order API
├── payment_service.py      # Service to process payments
├── inventory_service.py    # Service to manage inventory
├── email_service.py        # Service to send email confirmations
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── Dockerfile              # Docker configuration (if applicable)

# Installation
1. Clone the Repository
git clone https://github.com/your-username/rabbitmq-order-processing.git
cd rabbitmq1.1 
2. Install Dependencies
pip install -r requirements.txt
3. Set Up RabbitMQ
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management


# Usage
1. Running the Flask App
python app.py

2. Running the Consumer Services
In separate terminals, run the Payment Service, Inventory Service, and Email Service:
python payment_service.py
python inventory_service.py
python email_service.py

3. Testing the Order API
curl -X POST http://localhost:5000/api/orders -d '{"product_id": 1, "quantity": 2, "user_id": 100}' -H "Content-Type: application/json"

RabbitMQ Flow Explanation
1.Order Service publishes a message to RabbitMQ with the routing key order.created.
2.The Payment Service consumes the message, processes the payment, and sends a new message with the routing key payment.success.
3.The Inventory Service consumes the payment.success message, updates the inventory, and sends a message with the routing key inventory.updated.
4.Finally, the Email Service consumes the inventory.updated message and sends an email confirmation to the user.

# Testing
You can test the functionality of the entire system by:

1. Placing an order using the POST /api/orders endpoint.
2. Verifying that the Payment Service, Inventory Service, and Email Service process the order correctly in sequence:
Payment is successful.
Inventory is updated.
A confirmation email is sent.
You can view the logs of each service to ensure that each step is processed as expected.