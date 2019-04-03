FROM alpine:latest
RUN apk add --no-cache python3-dev
RUN pip3 install --upgrade pip
WORKDIR /docservice
COPY ./app /docservice
RUN pip3 install -r requirements.txt
EXPOSE 9101
WORKDIR /docservice/src
CMD ["python3", "__init__.py"]