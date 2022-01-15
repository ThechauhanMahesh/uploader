FROM ubuntu:20.04
RUN mkdir /app
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
WORKDIR /app
RUN apt -qq update --fix-missing
RUN apt -qq install -y git \
    python3 \
    python3-pip \
    wget \
    curl
RUN git clone https://github.com/aria2/aria2.git
COPY . .
RUN pip3 install -r requirements.txt
CMD ["bash","start.sh"]
