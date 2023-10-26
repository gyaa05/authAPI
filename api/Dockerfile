FROM python:3.11.4-alpine3.17
ENV TZ "Europe/Moscow"
WORKDIR /home/api
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev zbar zbar-dev
RUN python -m pip install --upgrade pip
ADD requirements.txt .
RUN pip install -U -r requirements.txt
ADD . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
