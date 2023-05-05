FROM python:3.7.8
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "handler.py"]
CMD ["pytest"]
