FROM ubuntu:latest
MAINTAINER Ilya Khramtsov <ilya@roothub.pw>
RUN apt-get update && apt-get install -yq --no-install-recommends python3 python3-pip python3-setuptools git && pip3 install wheel
RUN git clone https://github.com/nuBacuk/telegram-bot.git /telegram && pip3 install -r /telegram/bot/requirement.txt && chmod 777 /telegram/bot/bot.py && mkdir /data
RUN ln -s /telegram/bot/bot.py /usr/bin/bot.py
VOLUME /data
EXPOSE 8443
