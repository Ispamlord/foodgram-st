FROM python:3.12-slim

# Install system dependencies required for building Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0.0.0.0:8000"]

