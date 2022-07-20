FROM python:3.10.4


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /typing_speed_trainer

COPY . .
RUN pip install --no-cache-dir -r requirements/prod.txt && \
    rm -rf requirements

CMD python typing_speed_trainer/manage.py runserver 0.0.0.0:8000
