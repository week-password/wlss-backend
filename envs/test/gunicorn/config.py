accesslog = "-"  # here "-" means stdout

# gunicorn listens all connections but it's still secure
# since it's run in isolated docker network and only rev-proxy has access to it
bind = "0.0.0.0:8000"

errorlog = "-"  # here "-" means stdout

worker_class = "uvicorn.workers.UvicornWorker"

workers = 4

wsgi_app = "src.app:app"
