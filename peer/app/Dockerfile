FROM python:3.8-slim-buster

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt
RUN apt update -y && apt install net-tools -y
RUN apt-get install telnet

COPY ./app.py /app
COPY ./templates /app/templates
COPY ./module /app/

CMD [ "python", "app.py" ]