FROM    python:latest
LABEL   maintainer="Tin La <@tintinator>"

WORKDIR /app

COPY    requirements.txt /app/
RUN     pip install -r requirements.txt

COPY	ticker-company.csv /app/
COPY    *.py /app/
RUN     chmod a+x *.py

CMD  ["./main.py"]
