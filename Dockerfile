FROM python:3.9


WORKDIR /app

COPY prod_requirements.txt dev_requirements.txt /app/

RUN pip install -r prod_requirements.txt
RUN pip install -r dev_requirements.txt

COPY . /app

