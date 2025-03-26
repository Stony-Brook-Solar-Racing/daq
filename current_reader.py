import can

bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)

def read_can_messages():

    print("Listening for CAN messages...")

    while True:
        message = bus.recv()
        if message is not None:
            print(f"Received message: {message}")

if __name__ == "__main__":
    read_can_messages()
