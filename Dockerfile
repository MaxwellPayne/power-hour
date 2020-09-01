FROM python:3.7-stretch

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt update
RUN apt install -y nodejs

ADD ./requirements.txt /usr/src/app/
ADD ./powerhour /usr/src/app/powerhour/
ADD ./run_module.sh /usr/src/app/run_module.sh
ADD ./ui /usr/src/app/ui

WORKDIR /usr/src/app/ui
ARG ui_build_configuration=""
ENV UI_BUILD_CONFIGURATION=$ui_build_configuration
RUN /bin/bash build_ui.sh

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ENV LOG_LEVEL="INFO"
ENV PLAYLIST_URL=""
ENV YOUTUBE_API_KEY=""

EXPOSE 8000

CMD uvicorn powerhour.webserver.app:app --host 0.0.0.0
