FROM python:3.9.7 AS base

COPY user-agent.txt /home/root/.cache/instalooter/2.4.4/user-agent.txt

WORKDIR /app
RUN mkdir data

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app .

CMD python3 app.py