FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the application port
EXPOSE 8002

# Run the application
# CMD ["gunicorn", "--bind", "0.0.0.0:8002", "gym.wsgi:application"]
CMD ["gunicorn", "--bind", "0.0.0.0:8002", "--workers", "3", "--timeout", "120", "gym.wsgi:application"]

