FROM python:3
LABEL maintainer="Leonardo Takata"
COPY  requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD python3 app.py

