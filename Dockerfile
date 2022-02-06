FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
RUN apk add build-base
ENV STATIC_URL /static
ENV STATIC_PATH /app/application/static
ENV SECRET_KEY flask_app_secret_key
COPY ./requirements.txt /var/www/flask_app/
RUN pip install -r /var/www/flask_app/requirements.txt
