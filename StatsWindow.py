import time
import threading
import pm_common

from melee_common import *
from stats_common import *

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (100, 100, 100)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
yellow = (255, 255, 0)

# PLAYER_BLOCK = [TAGS_0, TAGS_1, TAGS_2, TAGS_3]


# def read_player_data(slot, pm, base_addr):
#     players = [PLAYER_ONE, PLAYER_TWO, PLAYER_THREE, PLAYER_FOUR]
#     player = base_addr + players[slot]
#     result = {}
#     for field_name, field_type in Playerblock._fields_:
#         # print("Field Name:", field_name)
#         # print("Field Type:", field_type)
#         if field_type is c_float:
#             ofst = get_field_offset(Playerblock, field_name)
#             result[field_name] = read_float(pm, player + ofst)
#         elif field_type is c_int:
#             ofst = get_field_offset(Playerblock, field_name)
#             if field_name == 'gobj':
#                 result[field_name] = pm.read_bytes(player + ofst, 4)[1:]
#                 result[field_name] = int.from_bytes(result[field_name], 'big')
#                 result[field_name] = result[field_name] + 0x80000000
#             else:
#                 result[field_name] = read_int(pm, player + ofst)
#         elif field_type is c_byte:
#             ofst = get_field_offset(Playerblock, field_name)
#             result[field_name] = pm.read_bytes(player + ofst, 1)
#             result[field_name] = int.from_bytes(result[field_name], byteorder='big')
#         elif field_type is c_short:
#             ofst = get_field_offset(Playerblock, field_name)
#             result[field_name] = read_short(pm, player + ofst)
#         elif field_type is Vec3:
#             ofst = get_field_offset(Playerblock, field_name)
#             result[field_name] = [
#                 read_float(pm, player + ofst),
#                 read_float(pm, (player + ofst + 4)),
#                 read_float(pm, (player + ofst + 8))
#             ]
#         else:
#             result[field_name] = None
#     return result


# def read_gobj_data(slot, pm, base_addr):
#     result = {}
#     for field_name, field_type in GOBJ._fields_:
#         if field_type is c_int:
#             result[field_name] = read_int(pm, base_addr + offset)
#         elif field_type is c_char:
#             result[field_name] = pm.read_bytes(base_addr + offset, 1)
#             # result[field_name] = int.from_bytes(result[field_name], byteorder='big')
#         elif field_type is c_short:
#             result[field_name] = read_short(pm, base_addr + offset)
#         elif field_type is c_int64:
#             result[field_name] = read_uint(pm, base_addr + offset)
#         else:
#             result[field_name] = None
#     return result


def map_data(field_name, value):
    if field_name == "state":
        state_map = {0: ("N/A", black), 1: ("N/A", black), 2: ("ACTIVE", white)}
        return state_map.get(value, ("Unk", black))
    elif field_name == "pkind":
        kind_map = {0: ("HMN", (250, 220, 255)), 1: ("CPU", grey),
                    2: ("DEMO", black), 3: ("N/A", black)}
        return kind_map.get(value, ("Unknown", None))
    elif field_name == "ckind":
        return CharacterKind._ids.get(value, "Unknown"), red
    elif field_name == "costume":
        return value, None
    elif field_name == "tag_pos":
        return value, magenta
    elif field_name == "spawn_pos":
        return value, magenta
    elif field_name == "respawn_pos":
        return value, magenta
    elif field_name == "gobj":
        value = hex(value)
        return value, white
    else:
        return value, None


def update_table_items():
    pm_common.resources_initialized.wait()
    pm = pm_common.pm
    GALE01 = pm_common.GALE01
    while True:
        color = white
        for block in range(4):
            # player_data = read_player_data(i, pm, GALE01)  # Read player data
            get_player_data(PLAYER_BLOCKS[block], block, pm, GALE01)
            for tag, field_name in PLAYER_TAGS[block].items():
                try:
                    value = getattr(PLAYER_BLOCKS[block], field_name)
                    if isinstance(value, Vec3):
                        value = [value.x, value.y, value.z]
                    if isinstance(value, GOBJ):
                        value = GOBJ.pointers.get('root')
                    mapped_value, color = map_data(field_name, value)
                    dpg.set_value(tag, mapped_value)  # Use the tag directly as the item ID
                    dpg.configure_item(tag, color=color)  # Use the tag directly as the item ID
                except KeyError:
                    # If the field name doesn't exist in player_data, skip it
                    continue
                except Exception as e:
                    # print(f"Error setting value for item {tag}: {e}")
                    continue
            # get_gobj_data(PLAYER_BLOCKS[i], i, pm)
        time.sleep(0.5)


def stats_window_close():
    dpg.set_viewport_width(400)


def stats_window():
    stats_main_id = "stats_main"
    _width = 500
    _height = 600
    if dpg.does_item_exist(stats_main_id):
        if not dpg.is_item_visible(stats_main_id):
            dpg.show_item(stats_main_id)
            vp_width = dpg.get_viewport_width()
            dpg.set_viewport_width(vp_width + _width - 1)
            return
        else:
            dpg.hide_item(stats_main_id)
            stats_window_close()
            return

    vp_width = dpg.get_viewport_width()
    dpg.set_viewport_width(vp_width + _width - 1)

    dpg.add_window(label="Stats", width=_width, height=_height, pos=[399, 0], no_move=True,
                   no_resize=True, no_collapse=True, on_close=stats_window_close, tag=stats_main_id)
    # with dpg.collapsing_header(label=f"Player", leaf=True, parent=stats_main_id):
    create_player_tables(stats_main_id)

    # dpg.set_value("stats_slot_type", "omg")
    # stage_stats = dpg.add_child_window(width=-1, height=-100, autosize_y=True, autosize_x=True, no_scrollbar=True, parent=stats_main_id)
    # dpg.add_text("Stage Stats", parent=stage_stats)
    update_thread = threading.Thread(target=update_table_items, daemon=True)
    update_thread.start()

