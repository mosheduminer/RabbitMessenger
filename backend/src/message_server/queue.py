from aio_pika import connect_robust, RobustConnection
from aio_pika.message import DeliveryMode, Message
from websockets.server import WebSocketServerProtocol


robust_connection: RobustConnection


async def create_connection():
    """
    Creates a connection to RabbitMQ.

    This function must be called before initializing the router
    """
    global robust_connection
    robust_connection = await connect_robust()


async def QueueConnection() -> RobustConnection:
    yield robust_connection


async def send_message_to_queue(
    queue_connection: RobustConnection, queue_name: str, message: bytes
):
    channel = queue_connection.channel()
    try:
        await channel.initialize()
        await channel.declare_queue(queue_name, durable=True)
        await channel.default_exchange.publish(
            Message(message, delivery_mode=DeliveryMode.PERSISTENT), queue_name
        )
    finally:
        await channel.close()


async def queue_message_subscribe(
    queue_connection: RobustConnection, queue_name: str, ws: WebSocketServerProtocol
):
    channel = queue_connection.channel()
    try:
        await channel.initialize()
        queue = await channel.declare_queue(queue_name, durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(requeue=True):
                    await ws.send(message.body)
    finally:
        # this will be triggered when the task the function runs in is cancelled
        await channel.close()
