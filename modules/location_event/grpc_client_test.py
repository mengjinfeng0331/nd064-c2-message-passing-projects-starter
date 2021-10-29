import location_pb2
import location_pb2_grpc
import grpc

"""
simulates client mobile app. Upload user location to the grpc server
"""

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

example_message_1 = location_pb2.LocationMessage(
    id=34567,
    person_id=12,
    longitude='-100',
    latitude='200',
    creation_time='2020-03-12',
)

example_message_2 = location_pb2.LocationMessage(
    id=3412567,
    person_id=123,
    longitude='1040',
    latitude='20',
    creation_time='2021-04-22',
)

response = stub.Create(example_message_1)
print('stub1 create for ', example_message_1)
response2 = stub.Create(example_message_2)
print('stub2 create for ', example_message_2)
