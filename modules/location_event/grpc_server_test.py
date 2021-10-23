from concurrent import futures

import location_pb2
import location_pb2_grpc
import grpc


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
        print('grpc create locationMessage: ', request_value)
        return location_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
server.wait_for_termination()
