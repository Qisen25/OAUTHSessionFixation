# Python image of the dockerized flask app
# atm i dont think it handles https but there are
# probs other ways to handle that

FROM python:3.8-alpine
WORKDIR /vulnerable_oauthapp
COPY flaskr/ flaskr/
WORKDIR flaskr/
RUN pip install -r requirements.txt
ENV FLASK_APP __init__.py
#CMD ["python","__init__.py"]
EXPOSE 5000
ENTRYPOINT ["sh", "boot.sh"] # Run the server on gunicorn which will also log server activity
