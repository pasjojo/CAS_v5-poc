FROM python:2
RUN pip install flask-oauthlib && mkdir /app
COPY app.py /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
