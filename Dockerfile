FROM    amd64/python:latest
LABEL   maintainer="Tin La <@tintinator>"

WORKDIR /app
COPY    requirements.txt /app/
RUN     pip install -r requirements.txt

COPY    stock_retrieval.py /app/
RUN     chmod a+x stock_retrieval.py

ENTRYPOINT  ["./stock_retrieval.py"]