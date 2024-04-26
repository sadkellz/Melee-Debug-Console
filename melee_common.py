from common import *
import pymem
import struct
import threading
import time

EMU_SIZE = 0x2000000
EMU_DIST = 0x10000

CAM_START = 0x453040
CAM_TYPE = 0x452C6F
GLOBAL_TIMER = 0x479D60
CPU_UPTIME = 0x4D7423
PAUSE_BIT = 0x479D68
PLAYER_ONE = 0x453080
PLAYER_TWO = 0x453F10
PLAYER_THREE = 0x454DA0
PLAYER_FOUR = 0x455C30

DEV_PAUSE = 0x479D68
FRAME_ADV = 0x479D6A
GAME_HUD = 0x4D6D58
STAGE_FLAGS = 0x453000
BG_COLOUR = 0x452C70


# Finds the specific page with the size of EMU_SIZE.
def pattern_scan_all(handle, pattern, *, return_multiple=False):
    next_region = 0
    found = []

    while next_region < 0x7FFFFFFF0000:
        next_region, page_found = pymem.pattern.scan_pattern_page(
            handle,
            next_region,
            pattern,
            return_multiple=return_multiple
        )

        if not return_multiple and page_found:
            if (next_region - page_found) == int(EMU_SIZE):
                return page_found

        if page_found:
            if (next_region - page_found) == int(EMU_SIZE):
                found += page_found

    if not return_multiple:
        return None

    return found


def error_handler(func):
    def wrapper(*args, **kwargs):
        global pymem_error
        global GALE01
        result = None  # Initialize result outside the try block

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            GALE01 = None
            pymem_error = True
            print(f"Error occurred: {e}")

        else:
            pymem_error = False  # Reset the global variable if no error occurred
        return result
    return wrapper


@error_handler
def find_pid():
    pids = ["Slippi Dolphin.exe", "Dolphin.exe"]
    for pid in pids:
        try:
            pm = pymem.Pymem(pid)
            print(pm)
            return pm
        except:
            continue
    print("Dolphin is not running or version is unsupported!")
    return None

GALE01 = None
pm = None

# Finds 'GALE01' in memory.
# This is used to jump to specific functions in Melee ie: GALE01 + CAM_START
def get_melee(pm):
    handle = pm.process_handle
    byte_pattern = bytes.fromhex("47 41 4C 45 30 31 00 02")
    GALE01 = pattern_scan_all(handle, byte_pattern)
    return GALE01


def check_melee():
    global pm
    global GALE01
    while True:
        pm = find_pid()
        if pm is None:
            GALE01 = None
            change_text_dolphin()
        elif pm and GALE01 is None:
            GALE01 = get_melee(pm)
            change_text_melee()
        if GALE01:
            gale01_cb()
            print("common", GALE01)
        time.sleep(1)  # Adjust the interval as needed

def change_text_dolphin():
    import MeleeDebugConsole
    MeleeDebugConsole.waiting_dolphin()

def change_text_melee():
    import MeleeDebugConsole
    MeleeDebugConsole.waiting_melee()


def gale01_cb():
    import MeleeDebugConsole  # Import main.py to access Dear PyGui functions
    MeleeDebugConsole.delete_error_popup()

thread = threading.Thread(target=check_melee)
thread.daemon = True  # Daemonize the thread so it stops when the main thread stops
thread.start()
def get_spawned_players():
    player_slots = {
        0: (GALE01 + PLAYER_ONE),
        1: (GALE01 + PLAYER_TWO),
        2: (GALE01 + PLAYER_THREE),
        3: (GALE01 + PLAYER_FOUR)
    }

    spawned_players = []
    player_address = []
    i = 0

    for player, state_address in player_slots.items():
        player_state = read_int(state_address)
        # if the player state isnt in-game, don't add
        if player_state == 2:
            spawned_players.append(player)
            player_address.append(state_address)
        i += 1

    return spawned_players, player_slots


# players, player_slots = get_spawned_players()


def get_player_data(pm, block):
    player = block
    gobj = pm.read_bytes(player + 0xB0, 4)[1:]
    gobj = int.from_bytes(gobj, 'big')
    gobj = GALE01 + gobj

    player_data = pm.read_bytes(gobj + 0x2C, 4)[1:]
    player_data = int.from_bytes(player_data, 'big')
    player_data = GALE01 + player_data
    player_data = pm.read_bytes(player_data, 4)[1:]
    player_data = int.from_bytes(player_data, 'big')
    player_data = GALE01 + player_data
    # print(pm.read_bytes(player_data, 4))
    return player_data


def update_bg_colour(pm, colour):
    colour_int = [int(c, 16) for c in colour]
    addr = GALE01 + BG_COLOUR
    print(colour_int)
    buf = struct.pack(">BBB", *colour_int)
    pm.write_bytes(addr, buf, len(buf))


def toggle_collision_overlay(pm, state):
    player_blocks = list(player_slots.values())
    slots = players
    byte = 1 if state else 2

    for slot in slots:
        current_block = player_blocks[slot]
        player_data = get_player_data(current_block)
        buf = struct.pack(">b", byte)
        pm.write_bytes(player_data + 0x225C, buf, len(buf))


def collision_overlay(pm, slot, byte):
    for player in players:
        if slot == player:
            player_blocks = list(player_slots.values())
            current_block = player_blocks[slot]
            player_data = get_player_data(current_block)
            buf = struct.pack(">b", byte)
            pm.write_bytes(player_data + 0x225C, buf, len(buf))


def toggle_pause(pm, state):
    addr = GALE01 + DEV_PAUSE
    byte = 0 if state else 1
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_hud(pm, state):
    addr = GALE01 + GAME_HUD
    byte = 0 if state else 1
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_pfx(pm, state):
    addr = GALE01 + STAGE_FLAGS
    byte = 0 if state else 0x10
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_bg(pm, state):
    addr = GALE01 + STAGE_FLAGS + 0x1
    byte = 0 if state else 0x4
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_stagevsl(pm, state):
    addr = GALE01 + STAGE_FLAGS + 0x1
    byte = 0 if state else 0x10
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_char_vis(pm, state):
    addr = GALE01 + STAGE_FLAGS
    byte = 0 if state else 0x80
    buf = struct.pack(">B", byte)
    pm.write_bytes(addr, buf, len(buf))


callbacks = {
    BTN_PAUSE:  toggle_pause,
    BTN_HUD:    toggle_hud,
    BTN_PFX:    toggle_pfx,
    BTN_VSB:    toggle_bg,
    BTN_VSL:    toggle_stagevsl,
    BTN_CVIS:   toggle_char_vis,
    BTN_CBBL:   toggle_collision_overlay,
}
