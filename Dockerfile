# Pull base image
FROM python:3.10.4-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for GDAL
RUN apt-get update && apt-get install -y \
    gdal-bin \
    python3-gdal \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files into the container
COPY . .

# Expose port if necessary (e.g., 8000 for Django)
EXPOSE 8000
