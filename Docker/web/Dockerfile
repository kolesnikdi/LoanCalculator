# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install netcat mc -y

# Set work directory
# Maine folder will be create with such name in docker container
WORKDIR /LoanCalculator

# Install dependencies
RUN pip3 install --upgrade pip
COPY /requirements.txt .
RUN pip3 install -r requirements.txt

# Copy project
COPY ../.. .
# Importante comande. Need for entrypoint.sh worck
CMD ["bash", "-c", "chmod", "+x", "/LoanCalculator/Docker/entrypoint.sh"]
ENTRYPOINT ["/LoanCalculator/Docker/entrypoint.sh"]
