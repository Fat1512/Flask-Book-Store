FROM python:3.10-slim-buster

WORKDIR /app

COPY /app .

RUN python -m pip install --upgrade pip
RUN python -m ensurepip --upgrade
RUN pip install setuptools
RUN pip install -r ./requirements.txt

CMD ["flask", "--app", "index.py", "run", "--debug", "--host=0.0.0.0"]