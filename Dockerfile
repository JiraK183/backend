FROM tiangolo/uvicorn-gunicorn:python3.9

ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app