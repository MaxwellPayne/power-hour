FROM python:3.7-stretch

ADD ./requirements.txt /usr/src/app/
ADD ./powerhour /usr/src/app/powerhour/

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ENV LOG_LEVEL="INFO"
ENV PLAYLIST_URL=""
ENV YOUTUBE_API_KEY=""

EXPOSE 8000

CMD python -m powerhour ${PLAYLIST_URL} --youtube-api-key=${YOUTUBE_API_KEY}
