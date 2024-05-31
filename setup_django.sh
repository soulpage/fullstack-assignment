#!/bin/bash

# Install python3-venv package
sudo apt update
sudo apt install -y python3-venv

# Create a directory for your Django project
mkdir my-django-app
cd my-django-app

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Django
pip install django

# Create a new Django project
django-admin startproject myproject .

# Create a new Django app
python manage.py startapp myapp

# Run database migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver

