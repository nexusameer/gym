# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (optimizes Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8002

# Ensure proper permissions
RUN chmod +x /app

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8002", "--workers", "3", "--timeout", "120", "--log-level", "info", "gym.wsgi:application"]
