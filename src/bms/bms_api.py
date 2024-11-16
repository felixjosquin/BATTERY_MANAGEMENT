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
