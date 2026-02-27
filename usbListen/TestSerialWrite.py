import serial
import time

# Change this to your actual port
PORT = '/dev/ttyUSB0'          # Linux
# PORT = 'COM4'                # Windows example

ser = serial.Serial(PORT, 115200, timeout=1)
print(f"Opened {ser.port} at 115200 baud")

try:
    print("Sending test messages every 1 second...")
    print("Press Ctrl+C to stop\n")

    counter = 0
    while True:
        msg = f"Test {counter} from PC -> STM32\r\n"
        ser.write(msg.encode('ascii'))           # send bytes
        print(f"Sent: {msg.strip()}")
        counter += 1
        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nStopped by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    ser.close()
    print("Port closed")