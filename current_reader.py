import can

def read_can_messages():
    bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)

    print("Listening for CAN messages...")

    while True:
        message = bus.recv()
        if message is not None:
            print(f"Received message: {message}")

if __name__ == "__main__":
    read_can_messages()
