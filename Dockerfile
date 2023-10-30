# Step 1: Use official lightweight Python image as base OS.
# FROM tiangolo/uvicorn-gunicorn:python3.10-slim

# Use an official Python runtime as the base image
FROM python:3.10

# Step 2. Copy local code to the container image.
WORKDIR /app
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Step 4: Run the web service on container startup using gunicorn webserver.
# ENV PORT=8080
# CMD exec gunicorn --bind :$PORT main:app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]