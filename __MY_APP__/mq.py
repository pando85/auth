import aiohttp

from aio_pika import connect_robust, DeliveryMode, IncomingMessage, Message

from __MY_APP__.config import RABBIT_HOST, RABBIT_USER, RABBIT_PASSWORD


async def send_message(channel, message_body):
    message = Message(
        message_body,
        delivery_mode=DeliveryMode.PERSISTENT
    )

    await channel.default_exchange.publish(
        message, routing_key='task_queue'
    )


def on_message(message: IncomingMessage):
    with message.process():
        print(" [x] Received message %r" % message)
        print("     Message body is: %r" % message.body)
        message.ack()


async def init_rabbit_client(app: aiohttp.web.Application) -> None:
    rabbit_url = f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}/"
    app['mq'] = {}
    app['mq']['connection'] = await connect_robust(rabbit_url)
    app['mq']['channel'] = await app['mq']['connection'].channel()

    queue = await app['mq']['channel'].declare_queue('hello')
    await queue.consume(on_message)
