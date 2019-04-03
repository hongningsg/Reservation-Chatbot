FROM alpine:latest
RUN apk add --no-cache python3-dev
RUN pip3 install --upgrade pip
WORKDIR /timeservice
COPY ./app /timeservice
RUN pip3 install -r requirements.txt
EXPOSE 9100
WORKDIR /timeservice/src
CMD python3 __init__.py