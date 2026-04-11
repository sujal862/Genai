from redis import Redis
from rq import Queue

redis_connection = Redis(
    host="full-rag_devcontainer-valkey-1",  # valkey container name
    port=6379
)

q = Queue(connection=redis_connection)
