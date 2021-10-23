import time
import os
import json

from concurrent import futures
from kafka import KafkaProducer

import location_pb2
import location_pb2_grpc
import grpc

kafka_url = os.environ["KAFKA_URL"]
kafka_topic = os.environ["KAFKA_TOPIC"]

producer = KafkaProducer(bootstrap_servers=kafka_url)


# accepts the grpc input and put them into the Kafka queue
class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        # To do: takes the grpc input and add them to the Kafka queue

        request_value = {
            'id': int(request.id),
            'person_id': int(request.person_id),
            'longitude': request.longitude,
            'latitude': request.latitude,
            'creation_time': request.creation_time
        }

        user_encode_data = json.dumps(request_value).encode('utf-8')
        producer.send(kafka_topic, user_encode_data)

        return location_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()
