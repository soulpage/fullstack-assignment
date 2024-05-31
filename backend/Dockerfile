FROM python:3.11-alpine

# Setting environment variables
ENV DJANGO_SECRET_KEY='7ktfs&84mqcw8^rgrhy!7d3y^7sq2=qqqxiifgckp0+kh160lj'
ENV FRONTEND_URL='http://3.91.91.222:3000'
# Set the working directory for the container
WORKDIR /fullstack-assignment/backend

# Copy the Python dependency file into the container
COPY dependencies.txt .

# Install Python dependencies
RUN python3.11 -m pip install -r dependencies.txt

# Copy the entire project into the container
COPY . .

# Copy the entrypoint.sh script into the container and make it executable
# COPY entrypoint.sh /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# Collect static files
RUN python3.11 manage.py collectstatic --noinput

# Expose the port that Django runs on
EXPOSE 8000

CMD ["python3.11","manage.py","runserver"]
