FROM ubuntu:20.04

RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN apt -qq update --fix-missing && \
    apt -qq install -y git \
    aria2 \
    python3-pip 
     
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["bash","start.sh"]
