import os

def getWorkers():
    workers = os.getenv('GUNICORN_WORKERS', 1)
    print("GUNICORN_WORKERS = ",workers)
    return workers

bind = '0.0.0.0:8888'
worker_connections = 10
keepalive = 5
timeout = 600
workers = getWorkers()

