FROM python:3.5 
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD graftmate_service/config/requirements.pip /config
RUN pip install -r graftmate_service/config/requirements.pip
RUN mkdir /src;
WORKDIR /src