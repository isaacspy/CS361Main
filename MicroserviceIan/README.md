How to Request Data:

1. Connect to the Microservice using ZeroMQ

This is done by setting up ZeroMQ context and a REQ socket on a port. For example a it might be helpful to make a function dedicated to sending data to the microservice.
Then, at the top of the function put the following:

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

This will create a socket operating over "tcp://localhost:5555" which you can replace if you have another ZeroMQ service running over that port.

2. Data Formatting

The microservice expects to receive a JSON with a list of exercise objects, each with a "name" and a list of weights as integers. 
As well as the units used for the weights, in the JSON this should be under "unit" as either "lbs" or "kgs".
Here is an example JSON I used to send to the microservice:

data = {
        "exercises": [
            {"name": "Bench Press", "weights": [100, 105, 110]},
            {"name": "Squat", "weights": [150, 160, 155]},
            {"name": "Deadlift", "weights": [200, 190, 195]}
        ],
        "unit": "lbs"
    }

3. Example Call

The call will be made using the socket with the .send method. The ZeroMQ .send method would not work with the string JSON.dumps gave me so I used the python .encode and .decode methods to the convert it from a string.
Here is an example call to the microservice following the initialization of the socket: 

socket.send(json.dumps(data).encode())


How to Receive Data:

1. Connect to the Microservice using ZeroMQ

This is done the same as if you were requesting. If you already intialized the socket and context in the same function you were requesting from do not reinitialize the socket.

2. Use the socket to receive the data.

This will be done using the .recv method. After the data is received you will have to decode the data and load it into a JSON object so it can be easily processed.
Here is an example call on how to receive data from the microservice:

response = socket.recv()
response_data = json.loads(response.decode())

This call will give you a JSON object with the same format as the request sorted and only including the max weight values as "max_weight".
Example response: 

data = {
        "exercises": [
            {"name": "Bench Press", "max_weight": 110},
            {"name": "Squat", "max_weight": 160},
            {"name": "Deadlift", "max_weight": 200}
        ],
        "unit": "lbs"
    }


UML Diagram:

