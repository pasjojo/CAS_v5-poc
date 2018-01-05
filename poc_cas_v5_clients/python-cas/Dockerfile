FROM python:3
RUN cd /tmp && git clone https://github.com/discogs/python-cas-client \
    && cd /tmp/python-cas-client \
    && pip3 install . \
    && pip3 install flask \
    && rm -Rf /tmp/python-cas-client  \
    && mkdir /app
COPY cas.py /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["cas.py"]
