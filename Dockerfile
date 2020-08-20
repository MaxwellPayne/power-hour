FROM python:3.7-stretch

ADD ./requirements.txt /usr/src/app/
ADD ./assets /usr/src/app/assets/
ADD ./powerhour /usr/src/app/powerhour/

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ENV PLAYLIST_URL=""
ENV YOUTUBE_API_KEY=""

CMD python -m powerhour ${PLAYLIST_URL} --youtube-api-key=${YOUTUBE_API_KEY}
