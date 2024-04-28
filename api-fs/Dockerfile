# Use the official Python image
FROM python:3.10

WORKDIR /app

# Add a non-root user and group
RUN addgroup myuser && adduser --disabled-password --gecos '' --ingroup myuser myuser && chsh -s /bin/sh myuser && chown -R myuser:myuser /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt update && apt upgrade -y && apt-get install -y build-essential


# Copy only the requirements file and install dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install -U setuptools pip \
    && pip install -r requirements.txt \
    && pip install redis

# Change the ownership to the created user and group
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

# Copy the entire application code
COPY . .

# Expose the port that Uvicorn will run on (adjust as needed)
EXPOSE 5000