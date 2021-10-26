FROM python:3.7

WORKDIR .
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT  ["python", "location_api.py"]