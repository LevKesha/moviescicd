# Dockerfile
FROM python:3.11

WORKDIR /app

# install app-level dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the application code
COPY movies.py .

# the Flask app listens on 605 (default in movies.py)
EXPOSE 605

CMD ["python", "movies.py"]
