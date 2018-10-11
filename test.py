import pika

credentials = pika.PlainCredentials('***', '***')
parameters = pika.ConnectionParameters(host='localhost',port=5672,\
    credentials=credentials, virtual_host='***')

def handle_delivery(body):
    """Called when we receive a message from RabbitMQ"""
    print(body)

def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    connection.channel(on_channel_open)    

def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.basic_recover(callback=handle_delivery,requeue=True)    

try:
    connection = pika.SelectConnection(parameters=parameters,\
        on_open_callback=on_connected)    

    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()
