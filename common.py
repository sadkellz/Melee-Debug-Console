import pymem
import struct


BTN_PAUSE = 45
BTN_HUD = 46
BTN_PFX = 47
BTN_VSB = 54
BTN_VSL = 55
BTN_CLR = -1
BTN_CVIS = 80
BTN_CBBL = 81

player_overlays = [100, 101, 102, 103]


def find_pid():
    pids = ["Slippi Dolphin.exe", "Dolphin.exe"]
    for pid in pids:
        try:
            pm = pymem.Pymem(pid)
            return pm
        except:
            continue
    print("Dolphin is not running or version is unsupported!")
    return None


pm = find_pid()


def read_int(address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>i', raw)[0]


def read_uint(address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>I', raw)[0]


def read_float(address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>f', raw)[0]


def read_short(address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>h', raw)[0]


def read_ushort(address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>H', raw)[0]


def read_long(address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>l', raw)[0]


def read_ulong(address):
    raw = pm.read_bytes(address, 4)
    return struct.unpack('>L', raw)[0]


def write_int(value, address):
    raw = struct.pack(">i", value)
    pm.write_bytes(address, raw, len(raw))


def write_uint(value, address):
    raw = struct.pack(">I", value)
    pm.write_bytes(address, raw, len(raw))


def write_float(value, address):
    raw = struct.pack(">f", value)
    pm.write_bytes(address, raw, len(raw))


def write_short(value, address):
    raw = struct.pack(">h", value)
    pm.write_bytes(address, raw, len(raw))


def write_ushort(value, address):
    raw = struct.pack(">H", value)
    pm.write_bytes(address, raw, len(raw))


def write_long(value, address):
    raw = struct.pack(">l", value)
    pm.write_bytes(address, raw, len(raw))


def write_ulong(value, address):
    raw = struct.pack(">L", value)
    pm.write_bytes(address, raw, len(raw))
