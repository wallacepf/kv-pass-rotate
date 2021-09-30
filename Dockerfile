FROM python:3.8.9-alpine

RUN apk update

WORKDIR /app

COPY *.py ./

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]