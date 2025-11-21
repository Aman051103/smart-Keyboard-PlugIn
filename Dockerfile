# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY runner.py .
COPY nexpree1.keras .
COPY tokenizer.pkl .

# Set environment variable for display (for GUI applications)
ENV DISPLAY=:0

# Run the application
CMD ["python", "runner.py"]

