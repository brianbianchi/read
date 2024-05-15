# Use an official Python runtime as a parent image
# FROM python:3.9
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install dependencies
# RUN apk update && apk add --no-cache python3 py3-pip

RUN pip install --no-cache-dir -r requirements.txt

# Copy the cron job file into the container
COPY crontab /etc/crontabs/root

# Expose the port the app runs on
EXPOSE 8000

# Copy the startup script to the container
# COPY start.sh /start.sh

# Set execute permissions for the startup script
# RUN chmod +x /start.sh

# Start the startup script in the foreground
# CMD ["/start.sh"]
CMD crond -f & python manage.py runserver 0.0.0.0:8000