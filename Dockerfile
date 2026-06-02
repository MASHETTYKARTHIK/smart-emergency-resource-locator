# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user for security
# We create a home directory because Streamlit stores config files in ~/.streamlit/
RUN useradd -m -u 1000 appuser

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and change ownership to the non-root user
COPY --chown=appuser:appuser . .

# Expose Streamlit port
EXPOSE 8501

# Healthcheck for the Streamlit app
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Switch to non-root user
USER appuser

# Run application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
