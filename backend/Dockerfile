FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY . .
CMD gunicorn core.wsgi:application --bind 0.0.0.0:8000