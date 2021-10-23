import location_pb2
import location_pb2_grpc
import grpc

"""
simulates client mobile app. Upload user location to the grpc server
"""

channel = grpc.insecure_channel("localhost:30003")
stub = location_pb2_grpc.LocationServiceStub(channel)

example_message_1 = location_pb2.LocationMessage(
    id=34567,
    person_id=12,
    longitude='-100',
    latitude='200',
    creation_time='2021-07-07 10:37:06.000000',
)

example_message_2 = location_pb2.LocationMessage(
    id=12567,
    person_id=32,
    longitude='1040',
    latitude='20',
    creation_time='2020-01-01 11:37:06.000000',
)

response = stub.Create(example_message_1)
response = stub.Create(example_message_2)
