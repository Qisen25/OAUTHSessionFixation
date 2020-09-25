# Python image of the dockerized flask app
# atm i dont think it handles https but there are
# probs other ways to handle that

FROM python:3.8-alpine
WORKDIR /vulnerable_oauthapp
COPY flaskr/ flaskr/
WORKDIR flaskr/
RUN apk add gcc musl-dev libffi-dev openssl-dev
RUN pip install -r requirements.txt
ENV FLASK_APP __init__.py
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
#CMD ["python","__init__.py"]
EXPOSE 5000
ENTRYPOINT ["sh", "boot.sh"] # Run the server on gunicorn which will also log server activity
