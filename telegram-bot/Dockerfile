# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy telegram bot requirements
COPY telegram-bot/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy telegram bot code
COPY telegram-bot/ .

# Command to run the telegram bot
CMD ["python", "app.py"]
