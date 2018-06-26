FROM ubuntu:latest
MAINTAINER Ilya Khramtsov <ilya@roothub.pw>
RUN apt-get update && apt-get -y install python3 python3-pip git
RUN git clone https://github.com/nuBacuk/telegram-bot.git /telegram && pip3 install -r /telegram/bot/requirement.txt && chmod 777 /telegram/bot/bot.py && mkdir /data
ADD token.cfg /telegram/bot/token.cfg
VOLUME /data
EXPOSE 8443
USER root
CMD python3 /telegram/bot/bot.py
