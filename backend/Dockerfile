FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET_KEY j0ddnj7lb$dnxga9(ea37*-qtb&j1h73wnz^mb)@c1qfw5!g8_
ENV FRONTEND_URL=http://127.0.0.1:3002


WORKDIR /django-app

COPY . /django-app

RUN pip install --no-cache-dir -r dependencies.txt

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

EXPOSE 8000

RUN pip install gunicorn

CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]
