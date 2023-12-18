# Use an official Node runtime as a base image
FROM node:14 AS frontend

# Set the working directory
WORKDIR /app

# Copy the frontend files to the container
COPY client/ .

# Install dependencies and build the production-ready frontend
RUN npm install
RUN npm run build

# Use an official Python runtime as a base image
FROM python:3.8 AS backend

# Set the working directory
WORKDIR /app

# Copy the backend files to the container
COPY app/ .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]
