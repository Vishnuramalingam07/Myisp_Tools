# Dockerfile for Google Cloud Run
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY refresh_server.py .
COPY ProdSanity_Report.py .
COPY database_utils.py .

# Expose port (Cloud Run uses PORT environment variable)
ENV PORT=8080
EXPOSE 8080

# Run the Flask server
CMD exec python refresh_server.py
