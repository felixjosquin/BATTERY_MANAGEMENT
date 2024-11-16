import serial
import bms

ser = serial.Serial(
    "/dev/ttyUSB0", baudrate=9600, timeout=1
)  # Replace '/dev/ttyUSB0' with your actual serial port

data_to_send = (
    b"\x7e\x32\x32\x30\x31\x34\x41\x34\x32\x45\x30\x30\x32\x30\x31\x46\x44\x32\x38\x0d"
)


def bms_parse_data(inc_data):
    SOI = hex(ord(inc_data[0:1]))
    VER = inc_data[1:3]
    ADR = inc_data[3:5]
    CID1 = inc_data[5:7]
    RTN = inc_data[7:9]
    LCHKSUM = inc_data[9:10]
    LENID = int(inc_data[10:13], 16)

    print("SOI: ", SOI)
    print("VER: ", VER)
    print("ADR: ", ADR)
    print("CID1: ", CID1)
    print("RTN: ", RTN)
    print("LENGTH: ", inc_data[9:13])
    print("LENID: ", LENID)
    print("LCHKSUM: ", LCHKSUM)

    INFO = inc_data[13 : 13 + LENID]
    CHKSUM = inc_data[13 + LENID : 13 + LENID + 4]
    print("INFO: ", INFO)
    print("CHKSUM: ", CHKSUM)
    print(inc_data[13 + LENID + 4 :])

    return INFO


def getAnologData(brutdata):
    byte_index = 2

    batt_soc = int(brutdata[byte_index : byte_index + 4], 16) / 100.0
    print("batt SoC : " + str(batt_soc) + " %")
    byte_index += 4
    print()

    batt_volt = int(brutdata[byte_index : byte_index + 4], 16) / 100.0
    print("batt volt: " + str(batt_volt) + " V")
    byte_index += 4
    print()

    nb_cells = int(brutdata[byte_index : byte_index + 2], 16)
    byte_index += 2
    for i in range(nb_cells):
        v = int(brutdata[byte_index : byte_index + 4], 16)
        print("Cell " + str(i + 1) + ": " + str(v) + " mV")
        byte_index += 4
    print()

    env_temp = int(brutdata[byte_index : byte_index + 4], 16) / 10
    print("ENV temp : " + str(env_temp))
    byte_index += 4
    print()

    pack_temp = int(brutdata[byte_index : byte_index + 4], 16) / 10
    print("pack temp : " + str(pack_temp))
    byte_index += 4
    print()

    mos_temp = int(brutdata[byte_index : byte_index + 4], 16) / 10
    print("MOS temp : " + str(mos_temp))
    byte_index += 4
    print()

    nb_temp = int(brutdata[byte_index : byte_index + 2], 16)
    byte_index += 2

    for j in range(nb_temp):
        temp = int(brutdata[byte_index : byte_index + 4], 16) / 10
        print("temp " + str(j + 1) + ": " + str(temp) + " deg")
        byte_index += 4
    print()

    value = int(brutdata[byte_index : byte_index + 4], 16)
    current = i / 100 if value < 32768 else (value - 65535) / 100
    print("current: " + str(current) + " A")
    byte_index += 4
    print()

    byte_index += 6

    soh = int(brutdata[byte_index : byte_index + 2], 16)
    print("soh: " + str(soh) + " %")
    byte_index += 2
    print()

    byte_index += 2

    full_cap = int(brutdata[byte_index : byte_index + 4], 16) / 100
    print("full_cap: " + str(full_cap) + " Ah")
    byte_index += 4
    print()

    remain_cap = int(brutdata[byte_index : byte_index + 4], 16) / 100
    print("remain_cap: " + str(remain_cap) + " Ah")
    byte_index += 4
    print()

    nb_cycle = int(brutdata[byte_index : byte_index + 4], 16)
    print("nb cycle: " + str(nb_cycle))
    byte_index += 4
    print()

    print(brutdata[byte_index:])


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
