from python:3.11

RUN pip install flask openai

RUN mkdir /app

WORKDIR /app

COPY ./script ./script

WORKDIR /app/script

ENV FLASK_APP=main.py
EXPOSE 5000

CMD ["flask", "run", "--host", "0.0.0.0"]
