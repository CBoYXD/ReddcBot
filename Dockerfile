FROM python:3.10

LABEL maintainer="https://github.com/CBoYXD" version="1.0.0"

WORKDIR /usr/src/reddc_bot

COPY . /usr/src/reddc_bot

RUN pip install --upgrade pip && \
    pip install --requirement requirements.txt

CMD ["python", "main.py"]