import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

data = {
    "exercises": [
        {"name": "Bench Press", "weights": [100, 105, 110]},
        {"name": "Squat", "weights": [150, 160, 155]}
    ],
    "unit": "lbs"
}

socket.send(json.dumps(data).encode())
print("data sent")

response = socket.recv()
response_data = json.loads(response.decode())
    
print("\nReceived response from microservice:")
print(json.dumps(response_data))