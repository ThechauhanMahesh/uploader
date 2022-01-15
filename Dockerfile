FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata

RUN mkdir ./app
WORKDIR /app

RUN apt -qq update --fix-missing
RUN apt -qq install -y git \
    python3 \
    python3-pip \
    aria2  
COPY . .
RUN pip3 install -r requirements.txt
CMD ["bash","start.sh"]
