FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./setup.cfg .
COPY ./setup.py .
RUN pip install --upgrade -e '.[dev]'

COPY . .

#WORKDIR /app

# RUN pip install hupper waitress
# CMD ["python", "run_api.py"]

