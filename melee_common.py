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
players = [PLAYER_ONE, PLAYER_TWO, PLAYER_THREE, PLAYER_FOUR]

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
        ("atk_count", c_int)
    ]
    FIELD_ADDRESSES = {
        "state": 0x00,
        "ckind": 0x00,
        "pkind": 0x00,
        "is_transformed": 0x00,
        "tag_pos": 0x00,
        "spawn_pos": 0x00,
        "respawn_pos": 0x00,
        "x34": 0x00,
        "x38": 0x00,
        "x3C": 0x00,
        "initial_facing": 0x00,
        "costume": 0x00,
        "x45": 0x00,
        "tint": 0x00,
        "team": 0x00,
        "controller": 0x00,
        "cpu_lvl": 0x00,
        "cpu_kind": 0x00,
        "handicap": 0x00,
        "x4C": 0x00,
        "kirby_copy": 0x00,
        "x4E": 0x00,
        "x4F": 0x00,
        "attack": 0x00,
        "kb": 0x00,
        "defense": 0x00,
        "scale": 0x00,
        "damage": 0x00,
        "initial_damage": 0x00,
        "stamina": 0x00,
        "falls": 0x00,
        "ko": 0x00,
        "x88": 0x00,
        "self_destructs": 0x00,
        "stocks": 0x00,
        "coins_curr": 0x00,
        "coins_total": 0x00,
        "x98": 0x00,
        "x9C": 0x00,
        "stick_smashes": 0x00,
        "tag": 0x00,
         # ("xA8": "0x00",
         # ("xAC_flags": "0x00",
         # ("xAC_80": "0x00",
         # ("is_multispawn": "0x00",
         # ("xAC_3f": "0x00",
         # ("xAD", "0x00",
         # ("xAE", "0x00",
         # ("xAF", "0x00",
        "xAC": 0x00,
        "gobj": 0x00,
        "sub_gobj": 0x00,
        "callback": 0x00,
        "stale_move": 0x00,
        "atk_count": 0x00,
    }


class GOBJ(Structure):
    _fields_ = [
        ("entity_class", c_short),
        ("p_link", c_char),
        ("gx_link", c_char),
        ("p_priority", c_char),
        ("gx_pri", c_char),
        ("obj_kind", c_char),
        ("data_kind", c_char),
        ("next", c_int),
        ("previous", c_int),
        ("nextOrdered", c_int),
        ("previousOrdered", c_int),
        ("proc", c_int),
        ("gx_cb", c_int),
        ("cobj_links", c_int64),
        ("hsd_object", c_int),
        ("userdata", c_int),
        ("destructor_function", c_int),
        ("unk_linked_list", c_int),
    ]
    FIELD_ADDRESSES = {
        "entity_class": 0x00,
        "p_link": 0x00,
        "gx_link": 0x00,
        "p_priority": 0x00,
        "gx_pri": 0x00,
        "obj_kind": 0x00,
        "data_kind": 0x00,
        "next": 0x00,
        "previous": 0x00,
        "nextOrdered": 0x00,
        "previousOrdered": 0x00,
        "proc": 0x00,
        "gx_cb": 0x00,
        "cobj_links": 0x00,
        "hsd_object": 0x00,
        "userdata": 0x00,
        "destructor_function": 0x00,
        "unk_linked_list": 0x00,
    }


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


# def get_player_data(pm, block, base_addr):
#     player = block
#     gobj = pm.read_bytes(player + 0xB0, 4)[1:]
#     gobj = int.from_bytes(gobj, 'big')
#     gobj = base_addr + gobj
#
#     player_data = pm.read_bytes(gobj + 0x2C, 4)[1:]
#     player_data = int.from_bytes(player_data, 'big')
#     player_data = base_addr + player_data
#     player_data = pm.read_bytes(player_data, 4)[1:]
#     player_data = int.from_bytes(player_data, 'big')
#     player_data = base_addr + player_data
#     # print(pm.read_bytes(player_data, 4))
#     return player_data


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


def get_field_offset(data_type, field_name):
    field_offset = getattr(data_type, field_name).offset
    return field_offset


PLAYER_BLOCKS = [Playerblock() for field_type in range(4)]
player1 = PLAYER_BLOCKS[0]
player1.state = 99
print(player1.state)

def get_player_data(playerblock, slot, pm, base_addr):
    result = {}
    player = base_addr + players[slot]
    for field_name, field_type in playerblock._fields_:
        if field_type is c_float:
            ofst = get_field_offset(Playerblock, field_name)
            result[field_name] = read_float(pm, player + ofst)
        elif field_type is c_int:
            ofst = get_field_offset(Playerblock, field_name)
            if field_name == 'gobj':
                result[field_name] = pm.read_bytes(player + ofst, 4)[1:]
                result[field_name] = int.from_bytes(result[field_name], 'big')
                result[field_name] = result[field_name] + 0x80000000
            else:
                result[field_name] = read_int(pm, player + ofst)
        elif field_type is c_byte:
            ofst = get_field_offset(Playerblock, field_name)
            result[field_name] = pm.read_bytes(player + ofst, 1)
            result[field_name] = int.from_bytes(result[field_name], byteorder='big')
        elif field_type is c_short:
            ofst = get_field_offset(Playerblock, field_name)
            result[field_name] = read_short(pm, player + ofst)
        elif field_type is Vec3:
            ofst = get_field_offset(Playerblock, field_name)
            result[field_name] = [
                read_float(pm, player + ofst),
                read_float(pm, (player + ofst + 4)),
                read_float(pm, (player + ofst + 8))
            ]
        else:
            result[field_name] = -1
        playerblock.FIELD_ADDRESSES[field_name] = result[field_name]

