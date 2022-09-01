#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(1):
    print(f"Sending request {request} ...")
    socket.send_string("1")

    #  Get the reply.
    message = socket.recv_string()
    print(f"Received reply {request} [ {message} ]")
	
    print(f"Sending request {request} ...")
    socket.send_string("2")

    #  Get the reply.
    message = socket.recv_string()
    print(f"Received reply {request} [ {message} ]")
	
    print(f"Sending request {request} ...")
    socket.send_string("3")

    #  Get the reply.
    message = socket.recv_string()
    print(f"Received reply {request} [ {message} ]")
	
    print(f"Sending request {request} ...")
    socket.send_string("+")

    #  Get the reply.
    message = socket.recv_string()
    print(f"Received reply {request} [ {message} ]")
	
    print(f"Sending request {request} ...")
    socket.send_string("-")

    #  Get the reply.
    message = socket.recv_string()
    print(f"Received reply {request} [ {message} ]")

    print(f"Sending request {request} ...")
    socket.send_string("r")

    #  Get the reply.
    message = socket.recv_string()
    print(f"Received reply {request} [ {message} ]")
