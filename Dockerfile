FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /kode
WORKDIR /kode
COPY requirements.txt /kode/
RUN apt-get update
RUN apt-get install -y apt-utils rsync
RUN pip install -r requirements.txt
COPY . /kode/


