from python:3.11

RUN pip install flask openai

RUN mkdir /app

WORKDIR /app

COPY ./public ./public
COPY ./script ./script

ENV FLASK_APP=script/main.py
EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
