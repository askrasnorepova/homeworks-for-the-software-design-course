import pika
import time
import asyncio
import logging
from fastapi import FastAPI
from app.routes import ml


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__) 

connection_params = pika.ConnectionParameters(
    host='http://localhost:15672/',
    port=5672,
    virtual_host='/',
    credentials=pika.PlainCredentials(
        username='rmuser',
        password='rmpassword'
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
queue_name = 'ml_task_queue'
channel.queue_declare(queue=queue_name)


# Функция, которая будет вызвана при получении сообщения
def callback(ch, method, body):
    app = FastAPI()
    app.include_router(route.ml)
    logger.info(f"Received: '{body}'")
    ch.basic_ack(delivery_tag=method.delivery_tag) # Ручное подтверждение обработки сообщения

# Подписка на очередь и установка обработчика сообщений
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=False  # Автоматическое подтверждение обработки сообщений
)

def get_session():
    db = next(get_session())
    try:
        yield db
    finally:
        db.close()

async def handle_message(message: pika.IncomingMessage):
    async with message.process():
        from request.Request import result
        data = result.loads(message.body.decode())

        request_id = data.get("request_id")
        result_data = data.get("result")

        with get_session() as db:
            (db, request_id, result_data)
            print(f"Результат для запроса {request_id} сохранён в базу.")
            
async def main():
    connection = await pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    queue = await channel.declare_queue("QuereRequest")
    
    await queue.consume(handle_message)
    
    print("Ожидание сообщений...")
    await asyncio.Future() 

if __name__ == "__main__":
    asyncio.run(main())