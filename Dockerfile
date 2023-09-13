FROM python:3.7-alpine
LABEL authors="markwiltshire"
LABEL maintainer="markjwiltshire@gmail.com"
WORKDIR /app
COPY rest_app.py /app
COPY db_connector.py /app
COPY globals.py /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
EXPOSE 5000
CMD python rest_app.py