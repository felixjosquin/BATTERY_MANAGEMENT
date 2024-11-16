import serial
import bms

ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)

try:
    sucess, data_to_send = bms.bms_encode_data(b"42", b"01")
    ser.write(data_to_send)
    response = ser.read_until(b"\x0d")
    sucess, info = bms.bms_decode_data(response)

finally:
    ser.close()
