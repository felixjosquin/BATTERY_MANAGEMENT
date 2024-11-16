import serial
import bms

ser = serial.Serial(
    "/dev/ttyUSB0", baudrate=9600, timeout=1
)  # Replace '/dev/ttyUSB0' with your actual serial port

data_to_send = (
    b"\x7e\x32\x32\x30\x31\x34\x41\x34\x32\x45\x30\x30\x32\x30\x31\x46\x44\x32\x38\x0d"
)

try:
    ser.write(data_to_send)
    # print("Data sent:", data_to_send)

    response = ser.read_until(b"\x0d")
    # print("Response: " + str(response))

    info = bms.bms_decode_data(response)

    # getAnologData(info)


finally:
    # Close the serial connection
    ser.close()
