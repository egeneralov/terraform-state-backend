FROM python:3

WORKDIR /app/

ADD requirements.txt /app/

RUN pip3 install --no-cache-dir -r /app/requirements.txt

ADD . .

cmd python app.py
