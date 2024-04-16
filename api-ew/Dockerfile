# Use the official Python image
FROM python:3.10.0-alpine


ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
COPY requirements.txt .
RUN pip install -U setuptools pip \
    && pip uninstall bson \
    && pip install -r requirements.txt \
    && pip install fastapi uvicorn

RUN addgroup -g $GROUP_ID www
RUN adduser -D -u $USER_ID -G www www -s /bin/sh


# Change the ownership to the created user and group
RUN chown -R www:www /var/www/


# Switch to the non-root user
USER www


COPY . .

# Expose the port that Uvicorn will run on (adjust as needed)
EXPOSE 8086

# Command to run the FastAPI application with Uvicorn
CMD ["python main.py"]
