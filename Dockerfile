FROM python:3.7-stretch

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt update
RUN apt install -y nodejs

ADD ./requirements.txt /usr/src/app/
ADD ./powerhour /usr/src/app/powerhour/
ADD ./ui /usr/src/app/ui

WORKDIR /usr/src/app/ui
RUN npm install
RUN npm run build -- --base-href=/ui/

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ENV LOG_LEVEL="INFO"
ENV PLAYLIST_URL=""
ENV YOUTUBE_API_KEY=""

EXPOSE 8000

CMD python -m powerhour ${PLAYLIST_URL} --youtube-api-key=${YOUTUBE_API_KEY}
