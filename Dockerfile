FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/metaparser
COPY ./bin /app/bin
COPY ./setup.* /app/

RUN pip install .

CMD [ "python", "/app/bin/metaparser" ]
