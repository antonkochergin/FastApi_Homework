FROM dh-mirror.gitverse.ru/library/python:3.11.11-alpine


ENV PATH="${PATH}:root/.local/bin"
COPY ./src /app/src
COPY ./alembic /app/alembic
COPY alembic.ini /app/
COPY requirements.txt /app/

RUN mkdir -p /app/data

ENV PYTHONPATH /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt --no-cache-dir

RUN chmod +x ./src/start.sh
EXPOSE 8000
