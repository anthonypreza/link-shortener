FROM arm32v7/python:3.8-buster

EXPOSE 80

WORKDIR /app

COPY requirements.txt .

RUN python -mvenv .venv

RUN .venv/bin/pip install -rrequirements.txt

COPY server ./server

CMD [".venv/bin/gunicorn", "server.app:app", "--bind", "0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker", "--log-level", "DEBUG"]