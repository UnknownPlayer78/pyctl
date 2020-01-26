import socket
from time import sleep
import ctypes

HOST = '127.0.0.1'
PORT = 8193

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

PRESSED     = [0] * 333
KEYS        = [0x0] * 333
KEYS[8]     = 0x0E # BACK
KEYS[9]     = 0x0F # TAB
KEYS[13]    = 0x1C # ENTER
KEYS[27]    = 0x01 # ESC
KEYS[32]    = 0x39 # SPACE
KEYS[44]    = 0x33 # COMMA
KEYS[45]    = 0x0C # MINUS
KEYS[46]    = 0x34 # PERIOD
KEYS[48]    = 0x52 # 0 (NUM)
KEYS[49]    = 0x02 # 1
KEYS[50]    = 0x03 # 2
KEYS[51]    = 0x04 # 3
KEYS[52]    = 0x05 # 4
KEYS[53]    = 0x06 # 5
KEYS[54]    = 0x07 # 6
KEYS[55]    = 0x08 # 7
KEYS[56]    = 0x09 # 8
KEYS[57]    = 0x0A # 9
KEYS[97]    = 0x1E # A
KEYS[98]    = 0x30 # B
KEYS[99]    = 0x2E # C
KEYS[100]   = 0x20 # D
KEYS[101]   = 0x12 # E
KEYS[102]   = 0x21 # F
KEYS[103]   = 0x22 # G
KEYS[104]   = 0x23 # H
KEYS[105]   = 0x17 # I
KEYS[106]   = 0x24 # J
KEYS[107]   = 0x25 # K
KEYS[108]   = 0x26 # L
KEYS[109]   = 0x32 # M
KEYS[110]   = 0x31 # N
KEYS[111]   = 0x18 # O
KEYS[112]   = 0x19 # P
KEYS[113]   = 0x10 # Q
KEYS[114]   = 0x13 # R
KEYS[115]   = 0x1F # S
KEYS[116]   = 0x14 # T
KEYS[117]   = 0x16 # U
KEYS[118]   = 0x2F # V
KEYS[119]   = 0x11 # W
KEYS[120]   = 0x2D # X
KEYS[121]   = 0x15 # Y
KEYS[122]   = 0x2C # Z
KEYS[273]   = 0xC8 # UP
KEYS[274]   = 0xD0 # DOWN
KEYS[275]   = 0xCD # RIGHT
KEYS[276]   = 0xCB # LEFT
KEYS[301]   = 0x3A # CAPS
KEYS[303]   = 0x36 # RSHIFT
KEYS[304]   = 0x2A # LSHIFT
KEYS[305]   = 0x9D # RCONTROL
KEYS[306]   = 0x1D # LCONTROL
KEYS[308]   = 0x38 # LMENU
KEYS[313]   = 0xB8 # RMENU

##### HU LAYOUT ######
KEYS[122]   = 0x15 # Y
KEYS[121]   = 0x2C # Z
######################

def press(key, state):
    if state == "1" and key != 300:
        if PRESSED[key] != state:
            PressKey(KEYS[key])
            PRESSED[key] = state
    elif state == "0" and key != 300:
        if PRESSED[key] != state:
            ReleaseKey(KEYS[key])
            PRESSED[key] = state

            if key == 301:
                PressKey(KEYS[key])
                ReleaseKey(KEYS[key])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        data = s.recv(512)
        try:
            pressed = data.decode().split(":")[1].split(";")[0]
        except:
            continue
        for key, state in enumerate(pressed):
            press(key, state)
