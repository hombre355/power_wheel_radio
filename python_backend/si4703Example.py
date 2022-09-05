#!/usr/bin/env python 2

# example program for testing the si4703 library
from si4703Library import si4703Radio
import zmq

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5556")

    # device ID is typically 0x10 - confirm with "sudo i2cdetect 1"
    radio = si4703Radio(0x10, 5, 19)
    radio.si4703Init()
    radio.si4703SetChannel(1035)
    radio.si4703SetVolume(5)
    print(str(radio.si4703GetChannel()))
    print(str(radio.si4703GetVolume()))

    try:
        while True:
            # check for stuff
            message = socket.recv_string()
            print("received request: %s" % message)

            if message == "1":
                radio.si4703SeekDown()
                socket.send_string(str(radio.si4703GetChannel()))
            if message == "2":
                radio.si4703SeekUp()
                socket.send_string(str(radio.si4703GetChannel()))
            if message == "3":
                radio.si4703SetChannel(1003)
                socket.send_string(str(radio.si4703GetChannel()))
            if message == "+":
                radio.si4703SetVolume(radio.si4703GetVolume() + 1)
                socket.send_string(str(radio.si4703GetVolume()))
            if message == "-":
                radio.si4703SetVolume(radio.si4703GetVolume() - 1)
                socket.send_string(str(radio.si4703GetVolume()))
            if message == "d":
                radio.si4703ClearRDSBuffers()
                radio.si4703GetRDSData()
                # print(test)
                socket.send_string("hi")
            if message == "t":
                print("connected to Iphone")
            if message == "r":
                break

    except KeyboardInterrupt:
        socket.send_string("Exiting program")

    socket.send_string("Shutting down radio")
    radio.si4703ShutDown()
    socket.send_string("Radio has been turned off")


if __name__ == "__main__":
    main()
