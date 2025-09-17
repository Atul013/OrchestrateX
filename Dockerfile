FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements-cloudrun.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY working_api.py .
COPY orche.env .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8080

# Run the application
CMD ["python", "working_api.py"]