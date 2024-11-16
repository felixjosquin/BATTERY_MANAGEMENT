import serial
import bms


try:
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1)
    bms.getAnologData(ser)
    # sucess, data_to_send = bms.bms_encode_data(b"42", b"01")
    # print(data_to_send)
    # ser.write(data_to_send)
    # response = ser.read_until(b"\x0d")
    # sucess, info = bms.bms_decode_data(response)

finally:
    ser.close()
