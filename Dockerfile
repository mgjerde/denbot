FROM python:3.9-alpine

RUN mkdir -p /app/data
RUN mkdir -p /app/src

COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

ADD src/ /app/src
WORKDIR /app/src

CMD [ "python", "main.py" ]
