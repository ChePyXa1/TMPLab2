from celery import Celery
import os

broker = f"amqp://guest:guest@{os.getenv('RABBITMQ_HOST','rabbitmq')}:5672/"
backend = None

app = Celery("worker", broker=broker, backend=backend)
