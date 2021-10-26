import os
import json

from kafka import KafkaConsumer
from sqlalchemy import create_engine
from geoalchemy2.functions import ST_AsText, ST_Point

KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]

DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_URL])


def write2db(location):
    engine = create_engine(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True)
    conn = engine.connect()

    _, person_id, longitude, latitude, creation_time = location
    coordinate = ST_Point(latitude, longitude)

    sql = "INSERT INTO location (person_id, coordinate, creation_time) VALUES ({}, {}}, {})" \
        .format(person_id, coordinate, creation_time)

    conn.execute(sql)


for message in consumer:
    message = message.value.decode()
    message = json.loads(message)
    print(message)
    write2db(message)



