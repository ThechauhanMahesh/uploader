FROM python:3.9
WORKDIR /app
RUN apt -qq update --fix-missing
RUN apt -qq install -y aria2
     
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["bash","./start.sh"]
