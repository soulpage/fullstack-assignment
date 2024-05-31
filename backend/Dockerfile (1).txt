# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET_KEY j0ddnj7lb$dnxga9(ea37*-qtb&j1h73wnz^mb)@c1qfw5!g8_
ENV FRONTEND_URL=http://127.0.0.1:3000


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r dependencies.txt

# Run migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port on which your Django app will run
EXPOSE 8000

# Install gunicorn
RUN pip install gunicorn


# Define the command to run your application
CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]
