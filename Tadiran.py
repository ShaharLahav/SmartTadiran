# import broadlink
# import argparse
# import time
import binascii
# import sys
# from . import ACProtocol
import logging

_LOGGER = logging.getLogger(__name__)


class Tadiran:

    HDR_MARK = 9650
    HDR_SPACE = 4825
    BIT_MARK = 620
    ONE_SPACE = 1600
    ZERO_SPACE = 540
    MSG_SPACE = 19000

     # Commands
    POWER_OFF = 'off'
    POWER_ON = 'on'

    # Operating modes
    MODE_AUTO = 'auto'
    MODE_HEAT = 'heat'
    MODE_COOL = 'cool'
    MODE_DRY = 'dry'
    MODE_FAN = 'fan'

    # Fan speeds. Note that some heatpumps have less than 5 fan speeds
    FAN_AUTO = 'auto'
    FAN_1 = 'low'
    FAN_2 = 'medium'
    FAN_3 = 'high'
    FAN_4 = 'higher'
    FAN_5 = 'highest'

    # Vertical air directions. Note that these cannot be set on all heat pumps
    VDIR_AUTO = 'auto'
    VDIR_MANUAL = 'manual'
    VDIR_UP = 'up'
    VDIR_MUP = 'middle_up'
    VDIR_MIDDLE = 'middle'
    VDIR_MDOWN = 'middle_down'
    VDIR_DOWN = 'down'
    VDIR_SWING = 'swing'
    VDIR_SWING_UP = 'swing_up'
    VDIR_SWING_MIDDLE = 'swing_middle'
    VDIR_SWING_DOWN = 'swing_down'

    # Horizontal air directions. Note that these cannot be set on all heat pumps
    HDIR_AUTO = 'auto'
    HDIR_MANUAL = 'manual'
    HDIR_MIDDLE = 'middle'
    HDIR_LEFT = 'left'
    HDIR_MLEFT = 'middle_left'
    HDIR_MRIGHT = 'middle_right'
    HDIR_RIGHT = 'right'
    HDIR_WIDE = 'wide'
    HDIR_SWING = 'swing'
    HDIR_SWING_SPREAD = 'swing_spread'


    TADIRAN_POWER_OFF = 0x00
    TADIRAN_POWER_ON = 0x08

    # Operating modes
    TADIRAN_MODE_AUTO = 0x00
    TADIRAN_MODE_HEAT = 0x04
    TADIRAN_MODE_COOL = 0x01
    TADIRAN_MODE_DRY = 0x02
    TADIRAN_MODE_FAN = 0x03

    # Fan speeds
    TADIRAN_FAN_AUTO = 0x00
    TADIRAN_FAN1 = 0x10
    TADIRAN_FAN2 = 0x20
    TADIRAN_FAN3 = 0x30

    # Only  available on YAN Vertical air directions
    TADIRAN_VDIR_AUTO = 0x00
    TADIRAN_VDIR_MANUAL = 0x00
    TADIRAN_VDIR_SWING = 0x01
    TADIRAN_VDIR_SWING_UP = 0xB
    TADIRAN_VDIR_SWING_MIDDLE = 0x9
    TADIRAN_VDIR_SWING_DOWN = 0x7
    TADIRAN_VDIR_UP = 0x02
    TADIRAN_VDIR_MUP = 0x03
    TADIRAN_VDIR_MIDDLE = 0x04
    TADIRAN_VDIR_MDOWN = 0x05
    TADIRAN_VDIR_DOWN = 0x06

    TADIRAN_HDIR_AUTO = 0
    TADIRAN_HDIR_LEFT = 0x20
    TADIRAN_HDIR_MLEFT = 0x30
    TADIRAN_HDIR_MIDDLE = 0x40
    TADIRAN_HDIR_MRIGHT = 0x50
    TADIRAN_HDIR_RIGHT = 0x60
    TADIRAN_HDIR_WIDE = 0xC0
    TADIRAN_HDIR_SWING = 0x10
    TADIRAN_HDIR_SWING_SPREAD = 0xD0
    MODEL = False

    op_modes = {
        MODE_AUTO: TADIRAN_MODE_AUTO,
        MODE_HEAT: TADIRAN_MODE_HEAT,
        MODE_COOL: TADIRAN_MODE_COOL,
        MODE_DRY: TADIRAN_MODE_DRY,
        MODE_FAN: TADIRAN_MODE_FAN,
    }

    fan_speeds = {
        FAN_AUTO: TADIRAN_FAN_AUTO,
        FAN_1: TADIRAN_FAN1,
        FAN_2: TADIRAN_FAN2,
        FAN_3: TADIRAN_FAN3,
    }

    swing_v_map = {
        VDIR_AUTO: TADIRAN_VDIR_AUTO,
        VDIR_MANUAL: TADIRAN_VDIR_MANUAL,
        VDIR_UP: TADIRAN_VDIR_UP,
        VDIR_MUP: TADIRAN_VDIR_MUP,
        VDIR_MIDDLE: TADIRAN_VDIR_MIDDLE,
        VDIR_MDOWN: TADIRAN_VDIR_MDOWN,
        VDIR_DOWN: TADIRAN_VDIR_DOWN,
        VDIR_SWING: TADIRAN_VDIR_SWING,
        VDIR_SWING_UP: TADIRAN_VDIR_SWING_UP,
        VDIR_SWING_MIDDLE: TADIRAN_VDIR_SWING_MIDDLE,
        VDIR_SWING_DOWN: TADIRAN_VDIR_SWING_DOWN,
    }

    swing_h_map = {
        HDIR_AUTO: TADIRAN_HDIR_AUTO,
        HDIR_MANUAL: TADIRAN_HDIR_AUTO,
        HDIR_MIDDLE: TADIRAN_HDIR_MIDDLE,
        HDIR_LEFT: TADIRAN_HDIR_LEFT,
        HDIR_MLEFT: TADIRAN_HDIR_MLEFT,
        HDIR_MRIGHT: TADIRAN_HDIR_MRIGHT,
        HDIR_RIGHT: TADIRAN_HDIR_RIGHT,
        HDIR_WIDE: TADIRAN_HDIR_WIDE,
        HDIR_SWING: TADIRAN_HDIR_SWING,
        HDIR_SWING_SPREAD: TADIRAN_HDIR_SWING_SPREAD,
    }

    def __init__(self):
        self.durations = []
        # ACProtocol.__init__(self)


    @classmethod
    def list_modes(cls):
        return list()

    @classmethod
    def list_fan_speeds(cls):
        return list()

    @classmethod
    def list_swing_modes(cls):
        return list()

    def get_durations(self):
        return self.durations

    @classmethod
    def is_swing(cls, vdir, hdir=HDIR_AUTO):
        return vdir in [cls.VDIR_SWING, cls.VDIR_SWING_DOWN, cls.VDIR_SWING_MIDDLE, cls.VDIR_SWING_UP] or \
               hdir in [cls.HDIR_SWING, cls.HDIR_SWING_SPREAD]

    def send_byte(self, val):
        for i in range(8):
            self.bit(val)
            val = val >> 1

    def mark(self, duration=-1):
        if duration == -1:
            duration = self.BIT_MARK
        self.durations.append(duration)

    def space(self, duration=-1):
        if duration == -1:
            duration = self.ZERO_SPACE
        self.durations.append(duration)

    def bit(self, val):
        self.durations.append(self.BIT_MARK)
        if val & 0x01:
            self.durations.append(self.ONE_SPACE)
        else:
            self.durations.append(self.ZERO_SPACE)

    @staticmethod
    def bit_reverse(val):
        x = val
        #          01010101  |         10101010
        x = ((x >> 1) & 0x55) | ((x << 1) & 0xaa)
        #          00110011  |         11001100
        x = ((x >> 2) & 0x33) | ((x << 2) & 0xcc)
        #          00001111  |         11110000
        x = ((x >> 4) & 0x0f) | ((x << 4) & 0xf0)
        return x

    def send(self, power_mode_cmd, operating_mode_cmd, fan_speed_cmd, temperature_cmd, swing_v_cmd, swing_h_cmd,
             turbo_mode=False):
        power_mode = self.TADIRAN_POWER_ON if power_mode_cmd == self.POWER_ON else self.TADIRAN_POWER_OFF
        operating_mode = self.op_modes.get(operating_mode_cmd, self.TADIRAN_MODE_HEAT)
        fan_speed = self.fan_speeds.get(fan_speed_cmd, self.TADIRAN_FAN_AUTO)
        swing = self.is_swing(swing_v_cmd, swing_h_cmd)
        swing_v = self.swing_v_map.get(swing_v_cmd, self.TADIRAN_VDIR_AUTO)
        swing_h = self.swing_h_map.get(swing_h_cmd, self.TADIRAN_HDIR_AUTO)
        temperature = 23
        if 15 < temperature_cmd < 31:
            temperature = temperature_cmd - 16
        self.durations = []
        self.send_tadiran(power_mode, operating_mode, fan_speed, temperature, swing, swing_v, swing_h,
                       turbo_mode)

    @staticmethod
    def make_data(power_mode, operating_mode, fan_speed, temperature, swing, swing_v, swing_h, turbo_mode=False):
        data = bytearray(8)
        swing_flag = 0x40 if swing else 0

        data[0] = fan_speed | operating_mode | power_mode | swing_flag
        data[1] = temperature
        data[2] = 0x70 if turbo_mode else 0x60
        data[3] = 0x50
        data[4] = swing_v | swing_h
        data[5] = 0x40
        data[6] = 0
        data[7] = (((data[0] & 0x0F) +
                    (data[1] & 0x0F) +
                    (data[2] & 0x0F) +
                    (data[3] & 0x0F) +
                    ((data[4] & 0xF0) >> 4) +
                    ((data[5] & 0xF0) >> 4) +
                    ((data[6] & 0xF0) >> 4) +
                    0x0A) & 0x0F) << 4
        return data

    def send_tadiran(self, power_mode, operating_mode, fan_speed, temperature, swing, swing_v, swing_h, turbo_mode=False):
        data = self.make_data(power_mode, operating_mode, fan_speed, temperature, swing, swing_v, swing_h, turbo_mode)

        self.send_train(data)

        data[3] = 0x70
        data[4] = 0
        data[5] = 0
        data[6] = 0
        data[7] = (((data[0] & 0x0F) +
                    (data[1] & 0x0F) +
                    (data[2] & 0x0F) +
                    (data[3] & 0x0F) +
                    ((data[4] & 0xF0) >> 4) +
                    ((data[5] & 0xF0) >> 4) +
                    ((data[6] & 0xF0) >> 4) +
                    0x0A) & 0x0F) << 4

        self.send_train(data)

    def send_train(self, data):
        for c in data:
            _LOGGER.debug("%02x" % c)
        self.mark(self.HDR_MARK)
        self.space(self.HDR_SPACE)
        for i in range(4):
            self.send_byte(data[i])
        # send what's left of byte 4
        self.bit(0)
        self.bit(1)
        self.bit(0)
        self.mark()
        self.space(self.MSG_SPACE)
        for i in range(4, 8):
            self.send_byte(data[i])
        self.mark()
        self.space(self.MSG_SPACE)
