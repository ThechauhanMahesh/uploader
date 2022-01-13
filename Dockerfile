FROM python:3.9
WORKDIR /app
RUN apt -qq update --fix-missing
RUN apt -qq install -y aria2
COPY . .
RUN pip install -r requirements.txt
CMD ["bash","./start.sh"]
