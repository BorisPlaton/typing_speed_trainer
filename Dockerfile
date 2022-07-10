FROM python:3.10.4

COPY . .
RUN pip install --no-cache-dir -r requirements/prod.txt && \
    rm -rf requirements
