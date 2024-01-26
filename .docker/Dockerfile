FROM python:3.11-slim-bookworm

# Upgrade system packages
RUN apt-get update && apt-get -y upgrade

# Switch to non-root user
RUN useradd --create-home appuser
USER appuser

# Install dependencies
WORKDIR /usr/app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .
CMD ["python", "-m", "app.main"]
