FROM python:3.11-slim-bullseye
WORKDIR /usr/src/bot
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./ .
CMD ["python", "main.py"]
