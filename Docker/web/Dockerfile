# Pull base image
FROM python:3.10.12-slim-bullseye

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
# Запуск з entrypoint.sh. в docker-compose.yml прибрати "command:"
#CMD ["bash", "-c", "chmod", "+x", "/LoanCalculator/Docker/entrypoint.sh"]
#ENTRYPOINT ["/LoanCalculator/Docker/entrypoint.sh"]

# те саме що і  23-24 стр. Варіант Запуску від Костянтина
#CMD ["chmod", "777", "./Docker/entrypoint.sh"]
#CMD ["bash", "-c", "chmod", "+x", "./Docker/entrypoint.sh"]
#ENTRYPOINT ["./Docker/entrypoint.sh"]