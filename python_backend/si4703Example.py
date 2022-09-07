#!/usr/bin/env python 2

# example program for testing the si4703 library
from si4703Library import si4703Radio
import zmq
from threading import Thread, Lock
import time


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5556")

    # device ID is typically 0x10 - confirm with "sudo i2cdetect 1"
    radio = si4703Radio(0x10, 5, 19)
    radio.si4703Init()
    radio.si4703SetChannel(1003)
    radio.si4703SetVolume(12)
    lock = Lock()

    print(str(radio.si4703GetChannel()))
    print(str(radio.si4703GetVolume()))
    thread = Thread(target=radio.si4703StoreRDSData, args=(lock,))
    thread.start()
    print("ready for commands")

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
                with lock:
                    socket.send_string(str(radio.si4703GetStationName()))
                    print(str(radio.si4703GetStationName()))
                    socket.send_string(str(radio.si4703GetSongName()))
                    print(str(radio.si4703GetSongName()))

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
