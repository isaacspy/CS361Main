import zmq
import json

def weights(workout_data):
    max_weights = []
    for exercise in workout_data['exercises']:
        max_weight = max(exercise['weights'])
        max_weights.append({'name': exercise['name'], 'max_weight': max_weight})
    max_weights.sort(key=lambda x: x['max_weight'], reverse=True)
    return max_weights

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://localhost:5555")
    print("Microservice running")
    
    while True:
        message = socket.recv()
        workout_data = json.loads(message.decode())
        
        max_weights = weights(workout_data)
        
        response = {
            'max_weights': max_weights,
            'unit': workout_data['unit']
        }
        
        socket.send(json.dumps(response).encode())

if __name__ == "__main__":
    main()