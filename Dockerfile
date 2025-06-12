# Use the standard Python 3.11 image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY movies.py .

# Expose port 80 and run
EXPOSE 80
CMD ["python", "movies.py"]
