FROM python:3.11-alpine
MAINTAINER ujwal.pachghare
WORKDIR /usr/bin/app
ENV PIP_NO_CACHE_DIR=1 \
    FRONTEND_URL="http://127.0.0.1:3000" \
    BACKEND_URL="http://127.0.0.1:8000" \
    BE_ADMIN_EMAIL="admin@admin.com" \
    BE_ADMIN_PASSWORD="admin" \
    DJANGO_SECRET_KEY="YWRtaW4="
RUN rm -rf /var/lib/apt/lists/*
ADD dependencies.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r dependencies.txt
COPY . .
RUN python manage.py collectstatic --no-input
RUN python manage.py migrate
EXPOSE 8000
CMD ["gunicorn","backend.wsgi:application","--bind","0.0.0.0:8000","--reload"]
