FROM python:3.8.18-alpine3.18
LABEL authors="markwiltshire"
LABEL maintainer="markjwiltshire@gmail.com"
ENV db_host=""
ENV db_port=""
ENV db_user=""
WORKDIR /app
COPY rest_app.py /app
COPY db_connector.py /app
COPY globals.py /app
COPY requirements.txt /app
# Add curl for healthcheck as it doesn't come in alpine
RUN apk --no-cache add curl
RUN apk update && apk upgrade
RUN pip install -r /app/requirements.txt
EXPOSE 5000
CMD ["sh", "-c", "python rest_app.py --db_host=$db_host --db_port=$db_port --db_user=$db_user"]