from common import *
import pymem
import struct
from ctypes import *

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


class Vec3(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float)]


class StaleMove(Structure):
    # Atk ID, Num of action states
    _fields_ = [
        ("current_index",   c_int),
        ("index_0",         c_short * 2),
        ("index_1",         c_short * 2),
        ("index_2",         c_short * 2),
        ("index_3",         c_short * 2),
        ("index_4",         c_short * 2),
        ("index_5",         c_short * 2),
        ("index_6",         c_short * 2),
        ("index_7",         c_short * 2),
        ("index_8",         c_short * 2),
        ("index_9",         c_short * 2),
    ]


class Playerblock(Structure):
    _fields_ = [
        ("state", c_int),
        ("ckind", c_int),
        ("pkind", c_int),
        ("is_transformed", c_byte * 2),
        ("tag_pos", Vec3),
        ("spawn_pos", Vec3),
        ("respawn_pos", Vec3),
        ("x34", c_int),
        ("x38", c_int),
        ("x3C", c_int),
        ("initial_facing", c_float),
        ("costume", c_byte),
        ("x45", c_byte),
        ("tint", c_byte),
        ("team", c_byte),
        ("controller", c_byte),
        ("cpu_lvl", c_byte),
        ("cpu_kind", c_byte),
        ("handicap", c_byte),
        ("x4C", c_byte),
        ("kirby_copy", c_byte),
        ("x4E", c_byte),
        ("x4F", c_byte),
        ("attack", c_float),
        ("kb", c_float),
        ("defense", c_float),
        ("scale", c_float),
        ("damage", c_short),
        ("initial_damage", c_short),
        ("stamina", c_short),
        ("falls", c_int * 2),
        ("ko", c_int * 6),
        ("x88", c_int),
        ("self_destructs", c_short),
        ("stocks", c_byte),
        ("coins_curr", c_int),
        ("coins_total", c_int),
        ("x98", c_int),
        ("x9C", c_int),
        ("stick_smashes", c_int * 2),
        ("tag", c_int),
        # ("xA8", c_int),
        # ("xAC_flags", c_byte),
        # ("xAC_80", c_byte, 1),
        # ("is_multispawn", c_byte, 1),
        # ("xAC_3f", c_byte, 6),
        # ("xAD", c_byte),
        # ("xAE", c_byte),
        # ("xAF", c_byte),
        ("xAC", c_int),
        ("gobj", c_int),
        ("sub_gobj", c_int),
        ("callback", c_int),
        ("stale_move", StaleMove),
        ("atk_count", c_int),
    ]


class CharacterKind:
    _ids = {
        0: "Captain Falcon",
        1: "Donkey Kong",
        2: "Fox",
        3: "Mr.Game & Watch",
        4: "Kirby",
        5: "Bowser",
        6: "Link",
        7: "Luigi",
        8: "Mario",
        9: "Marth",
        10: "Mewtwo",
        11: "Ness",
        12: "Peach",
        13: "Pikachu",
        14: "Ice Climbers",
        15: "Jigglypuff",
        16: "Samus",
        17: "Yoshi",
        18: "Zelda",
        19: "Sheik",
        20: "Falco",
        21: "Young Link",
        22: "Dr.Mario",
        23: "Roy",
        24: "Pichu",
        25: "Ganondorf",
        26: "Master Hand",
        27: "Wireframe Male(Boy)",
        28: "Wireframe Female(Girl)",
        29: "Giga Bowser",
        30: "Crazy Hand",
        31: "Sandbag",
        32: "Popo",
        33: "User Select",
    }


def get_spawned_players(pm, base_addr):
    player_slots = {
        0: (base_addr + PLAYER_ONE),
        1: (base_addr + PLAYER_TWO),
        2: (base_addr + PLAYER_THREE),
        3: (base_addr + PLAYER_FOUR)
    }

    spawned_players = []
    player_address = []
    i = 0

    for player, state_address in player_slots.items():
        player_state = read_int(pm, state_address)
        # if the player state isnt in-game, don't add
        if player_state == 2:
            spawned_players.append(player)
            player_address.append(state_address)
        i += 1

    return spawned_players, player_slots


def get_player_data(pm, block, base_addr):
    player = block
    gobj = pm.read_bytes(player + 0xB0, 4)[1:]
    gobj = int.from_bytes(gobj, 'big')
    gobj = base_addr + gobj

    player_data = pm.read_bytes(gobj + 0x2C, 4)[1:]
    player_data = int.from_bytes(player_data, 'big')
    player_data = base_addr + player_data
    player_data = pm.read_bytes(player_data, 4)[1:]
    player_data = int.from_bytes(player_data, 'big')
    player_data = base_addr + player_data
    # print(pm.read_bytes(player_data, 4))
    return player_data


def update_bg_colour(colour, pm, base_addr):
    colour_int = [int(c, 16) for c in colour]
    addr = base_addr + BG_COLOUR
    print(colour_int)
    buf = struct.pack(">BBB", *colour_int)
    pm.write_bytes(addr, buf, len(buf))


def toggle_collision_overlay(state, pm, base_addr):
    players, player_slots = get_spawned_players(pm, base_addr)
    player_blocks = list(player_slots.values())
    slots = players
    byte = 1 if state else 2

    for slot in slots:
        current_block = player_blocks[slot]
        player_data = get_player_data(pm, current_block, base_addr)
        buf = struct.pack(">b", byte)
        pm.write_bytes(player_data + 0x225C, buf, len(buf))


def collision_overlay(slot, val, pm, base_addr):
    players, player_slots = get_spawned_players(pm, base_addr)
    for player in players:
        if slot == player:
            player_blocks = list(player_slots.values())
            current_block = player_blocks[slot]
            player_data = get_player_data(pm, current_block, base_addr)
            current_flag = int.from_bytes(pm.read_bytes(player_data + 0x225C, 1), byteorder='big')

            print(val)
            if val <= 3:
                mask = 0b11111100
                current_flag &= mask
                current_flag |= val
            elif val == 4:
                current_flag |= (1 << 2)
                current_flag &= ((1 << (val - 2)) | ((1 << 2) - 1))
            elif 4 < val < 10:
                current_flag |= (1 << (val - 2))
                current_flag &= ((1 << (val - 2)) | ((1 << 2) - 1))
            elif val == 99:
                current_flag &= ((1 << 1) | (1 << 0))

            buf = struct.pack(">B", current_flag)
            pm.write_bytes(player_data + 0x225C, buf, len(buf))


def toggle_pause(state, pm, base_addr):
    addr = base_addr + DEV_PAUSE
    byte = 0 if state else 1
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_hud(state, pm, base_addr):
    addr = base_addr + GAME_HUD
    byte = 0 if state else 1
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_pfx(state, pm, base_addr):
    addr = base_addr + STAGE_FLAGS
    byte = 0 if state else 0x10
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_bg(state, pm, base_addr):
    addr = base_addr + STAGE_FLAGS + 0x1
    byte = 0 if state else 0x4
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_stagevsl(state, pm, base_addr):
    addr = base_addr + STAGE_FLAGS + 0x1
    byte = 0 if state else 0x10
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


def toggle_char_vis(state, pm, base_addr):
    addr = base_addr + STAGE_FLAGS
    byte = 0 if state else 0x80
    buf = struct.pack(">B", byte)
    pm.write_bytes(addr, buf, len(buf))


def frame_adv(state, pm, base_addr):
    addr = base_addr + FRAME_ADV
    byte = 1
    buf = struct.pack(">b", byte)
    pm.write_bytes(addr, buf, len(buf))


callbacks = {
    BTN_PAUSE:  toggle_pause,
    BTN_HUD:    toggle_hud,
    BTN_PFX:    toggle_pfx,
    BTN_ADV:    frame_adv,
    BTN_VSB:    toggle_bg,
    BTN_VSL:    toggle_stagevsl,
    BTN_CVIS:   toggle_char_vis,
    BTN_CBBL:   toggle_collision_overlay,
}


def get_field_offset(field_name):
    field_offset = getattr(Playerblock, field_name).offset
    return field_offset




