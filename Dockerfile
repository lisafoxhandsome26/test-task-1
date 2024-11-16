FROM python:3.12.3-alpine3.20

WORKDIR /src

COPY /backend .

COPY /requirements .
COPY /main.py .
RUN pip install --upgrade pip "poetry==1.8.3"
RUN poetry config virtualenvs.create false --local
RUN poetry install
