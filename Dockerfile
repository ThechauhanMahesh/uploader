ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
FROM ubuntu:20.04
RUN mkdir ./app
RUN chmod 777 ./app
WORKDIR /app
RUN apt -qq update --fix-missing
RUN apt -qq install -y aria2 \
    python3 \
    python3-pip
COPY . .
RUN pip install -r requirements.txt
CMD ["bash","start.sh"]
