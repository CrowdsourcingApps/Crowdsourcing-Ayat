# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt 
RUN apt-get update && apt-get install -y \
curl && apt-get clean && apt-get install ffmpeg -y

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser --disabled-password appuser
RUN chown -R appuser:appuser /app
RUN chmod 755 /app
USER appuser

# Healthcheack
HEALTHCHECK --interval=5s --timeout=3s CMD curl --fail http://localhost:8000/docs || exit 1  

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn","src.main:app", "--reload","--host","0.0.0.0"]
