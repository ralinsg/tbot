FROM python:3.7-slim

LABEL author="ralinsg" version='0.1' release_date='10.12.2022'

RUN mkdir -p /var/scr/app

WORKDIR /usr/scr/app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /usr/scr/app

CMD ['python', 'bot_telegram']
