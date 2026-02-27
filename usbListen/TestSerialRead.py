import serial
import time

# Configure your port
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Change COM3 to your port
ser.flushInput()

print("Listening on", ser.port)
print("Press Ctrl+C to stop\n")

try:
    while True:
        if ser.in_waiting > 0:  # Check if data available
            data = ser.read(ser.in_waiting)
            print(f"Received {len(data)}")  # Print as hex
            print(f"{data}")  # Print as text (if printable)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped")
    ser.close()
