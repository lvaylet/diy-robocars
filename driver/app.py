#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Consume steering and throttle orders and drive motors through PCA9685.
"""

import logging
import os

import pika

# region Logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# endregion

# region Data broker (RabbitMQ)
RABBITMQ_USERNAME = os.environ.get('RABBITMQ_USERNAME', 'guest')
RABBITMQ_PASSWORD = os.environ.get('RABBITMQ_PASSWORD', 'guest')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.environ.get('RABBITMQ_PORT', '5672'))
RABBITMQ_QUEUE = os.environ.get('RABBITMQ_QUEUE', 'steering_and_throttle')

credentials = pika.PlainCredentials(username=RABBITMQ_USERNAME,
                                    password=RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBITMQ_HOST,
                                       port=RABBITMQ_PORT,
                                       virtual_host='/',
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue=RABBITMQ_QUEUE)


def callback(ch, method, properties, body):
    logging.info('Received %r', body)


channel.basic_consume(callback,
                      queue=RABBITMQ_QUEUE,
                      no_ack=True)

# With topics:
# channel.exchange_declare(exchange='topic_rc_receiver_pulse_widths_microseconds',
#                          exchange_type='topic')


# endregion

logger.info('Consuming normalized steering and throttle orders. Press CTRL+C to exit.')
channel.start_consuming()
