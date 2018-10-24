import Tadiran
import broadlink
import binascii

TICK = 32.6
IR_TOKEN = 0x26


def convert_bl(durations):
    result = bytearray()
    result.append(IR_TOKEN)
    result.append(0)  # repeat
    result.append(len(durations) % 256)
    result.append(int(len(durations) / 256))
    for dur in durations:
        num = int(round(dur / TICK))
        if num > 255:
            result.append(0)
            result.append(int(num / 256))
        result.append(num % 256)
    result.append(0x0d)
    result.append(0x05)
    result.append(0x00)
    result.append(0x00)
    result.append(0x00)
    result.append(0x00)
    return result


def format_durations(data):
    result = ''
    for i in range(0, len(data)):
        if len(result) > 0:
            result += ' '
        result += ('+' if i % 2 == 0 else '-') + str(data[i])
    return result


if __name__ == '__main__':
    Sender = Tadiran.Tadiran #hvac_ir.get_sender('tadiran')

    if Sender is None:
        print("Unknown sender")
        exit(2)
    g = Sender()
    g.send(Sender.POWER_OFF, Sender.MODE_COOL, Sender.FAN_AUTO, 22, Sender.VDIR_MANUAL,
           Sender.HDIR_SWING, False)
    durations = g.get_durations()
    # print(format_durations(durations))

    # Uncommend the following to send code over Broadlink:

    BROADLINK_IP = '192.168.1.169'
    BROADLINK_MAC = '78:0F:77:17:EA:6A'

    fan_speeds = [("auto", 0), ("low", 0x10), ("mid",0x20), ("high",0x30) ]



    for fan in fan_speeds:
        for temp in range(16,30,1):
            g.send(Sender.POWER_ON, Sender.MODE_HEAT, fan[0], temp, Sender.VDIR_MANUAL, Sender.HDIR_SWING, False)
            durations = g.get_durations()
            bl = convert_bl(durations)
            bll = str(binascii.b2a_base64(bl)).replace("\\n", "").replace("'","")
            print str(fan[0]) + "_" + str(temp) + " = " + bll

    print "-----------------------------------------------"
    # bl = convert_bl(durations)
    # bll = str(binascii.b2a_base64(bl)).replace("\\n", "")[1:].replace("'","")

    # print(binascii.b2a_hex(bl))
    # mac = binascii.unhexlify(BROADLINK_MAC.encode().replace(b':', b''))
    # dev = broadlink.rm((BROADLINK_IP, 80), mac, devtype=0x272a)
    # dev.auth()
    # dev.send_data(bl)
