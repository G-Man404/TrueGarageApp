# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project
COPY . /code/