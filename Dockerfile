FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY env/.env .
COPY ./requirements/prod.txt .
COPY ./scripts/entrypoint.sh .
ENTRYPOINT ["sh", "entrypoint.sh"]

RUN pip install --no-cache-dir -r prod.txt && rm -f prod.txt

COPY ./typing_speed_trainer .

