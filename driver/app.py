#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Consume steering and throttle orders and drive motors through PCA9685.
"""

import logging

import pika

# region Logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# endregion

# region Data broker (RabbitMQ)

credentials = pika.PlainCredentials(username='guest',
                                    password='guest')
parameters = pika.ConnectionParameters(host='rabbitmq',
                                       port=5672,
                                       virtual_host='/',
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='pulse_width_microseconds')


def callback(ch, method, properties, body):
    logging.info('Received %r', body)


channel.basic_consume(callback,
                      queue='pulse_width_microseconds',
                      no_ack=True)

# With topics:
# channel.exchange_declare(exchange='topic_rc_receiver_pulse_widths_microseconds',
#                          exchange_type='topic')


# endregion

logger.info('Consuming steering and throttle orders. Press CTRL+C to exit.')
channel.start_consuming()
