import dearpygui.dearpygui as dpg
TAGS_0 = {
    8000: "state",
    8001: "ckind",
    8002: "pkind",
    8003: "tag_pos",
    8004: "spawn_pos",
    8005: "respawn_pos",
    8006: "costume",
    8007: "tint",
    8008: "team",
    8009: "controller",
    8010: "cpu_lvl",
    8011: "cpu_kind",
    8012: "handicap",
    8013: "kirby_copy",
    8014: "attack",
    8015: "kb",
    8016: "defense",
    8017: "scale",
    8018: "damage",
    8019: "initial_damage",
    8020: "stamina",
    8021: "falls",
    8022: "ko",
    8023: "x88",
    8024: "self_destructs",
    8025: "stocks",
    8026: "coins_curr",
    8027: "coins_total",
    8028: "x98",
    8029: "x9C",
    8030: "stick_smashes",
    8031: "tag",
    8032: "xAC",
    8033: "gobj",
    8034: "sub_gobj",
    8035: "callback",
    8036: "stale_move",
    8037: "atk_count",
}

TAGS_1 = {
    8100: "state",
    8101: "ckind",
    8102: "pkind",
    8103: "tag_pos",
    8104: "spawn_pos",
    8105: "respawn_pos",
    8106: "costume",
    8107: "tint",
    8108: "team",
    8109: "controller",
    8110: "cpu_lvl",
    8111: "cpu_kind",
    8112: "handicap",
    8113: "kirby_copy",
    8114: "attack",
    8115: "kb",
    8116: "defense",
    8117: "scale",
    8118: "damage",
    8119: "initial_damage",
    8120: "stamina",
    8121: "falls",
    8122: "ko",
    8123: "x88",
    8124: "self_destructs",
    8125: "stocks",
    8126: "coins_curr",
    8127: "coins_total",
    8128: "x98",
    8129: "x9C",
    8130: "stick_smashes",
    8131: "tag",
    8132: "xAC",
    8133: "gobj",
    8134: "sub_gobj",
    8135: "callback",
    8136: "stale_move",
    8137: "atk_count",
}

TAGS_2 = {
    8200: "state",
    8201: "ckind",
    8202: "pkind",
    8203: "tag_pos",
    8204: "spawn_pos",
    8205: "respawn_pos",
    8206: "costume",
    8207: "tint",
    8208: "team",
    8209: "controller",
    8210: "cpu_lvl",
    8211: "cpu_kind",
    8212: "handicap",
    8213: "kirby_copy",
    8214: "attack",
    8215: "kb",
    8216: "defense",
    8217: "scale",
    8218: "damage",
    8219: "initial_damage",
    8220: "stamina",
    8221: "falls",
    8222: "ko",
    8223: "x88",
    8224: "self_destructs",
    8225: "stocks",
    8226: "coins_curr",
    8227: "coins_total",
    8228: "x98",
    8229: "x9C",
    8230: "stick_smashes",
    8231: "tag",
    8232: "xAC",
    8233: "gobj",
    8234: "sub_gobj",
    8235: "callback",
    8236: "stale_move",
    8237: "atk_count",
}

TAGS_3 = {
    8300: "state",
    8301: "ckind",
    8302: "pkind",
    8303: "tag_pos",
    8304: "spawn_pos",
    8305: "respawn_pos",
    8306: "costume",
    8307: "tint",
    8308: "team",
    8309: "controller",
    8310: "cpu_lvl",
    8311: "cpu_kind",
    8312: "handicap",
    8313: "kirby_copy",
    8314: "attack",
    8315: "kb",
    8316: "defense",
    8317: "scale",
    8318: "damage",
    8319: "initial_damage",
    8320: "stamina",
    8321: "falls",
    8322: "ko",
    8323: "x88",
    8324: "self_destructs",
    8325: "stocks",
    8326: "coins_curr",
    8327: "coins_total",
    8328: "x98",
    8329: "x9C",
    8330: "stick_smashes",
    8331: "tag",
    8332: "xAC",
    8333: "gobj",
    8334: "sub_gobj",
    8335: "callback",
    8336: "stale_move",
    8337: "atk_count",
}

TAGS_4 = {
    8400: "state",
    8401: "ckind",
    8402: "pkind",
    8403: "tag_pos",
    8404: "spawn_pos",
    8405: "respawn_pos",
    8406: "costume",
    8407: "tint",
    8408: "team",
    8409: "controller",
    8410: "cpu_lvl",
    8411: "cpu_kind",
    8412: "handicap",
    8413: "kirby_copy",
    8414: "attack",
    8415: "kb",
    8416: "defense",
    8417: "scale",
    8418: "damage",
    8419: "initial_damage",
    8420: "stamina",
    8421: "falls",
    8422: "ko",
    8423: "x88",
    8424: "self_destructs",
    8425: "stocks",
    8426: "coins_curr",
    8427: "coins_total",
    8428: "x98",
    8429: "x9C",
    8430: "stick_smashes",
    8431: "tag",
    8432: "xAC",
    8433: "gobj",
    8434: "sub_gobj",
    8435: "callback",
    8436: "stale_move",
    8437: "atk_count",
}



def create_player_table(slot, parent, tag):
    with dpg.collapsing_header(label=f"Player {slot+1}", parent=parent, leaf=True):
        with dpg.tree_node(label="Info"):
            with dpg.table(header_row=False, borders_innerH=False, borders_outerH=True,
                           borders_innerV=True, borders_outerV=True):
                dpg.add_table_column()

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"State: ")
                        dpg.add_text("def", color=(255, 0, 0), tag=tag)

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Character: ")
                        dpg.add_text("def", color=(255, 0, 0), tag=(tag+1))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Slot Type: ")
                        dpg.add_text("def", color=(255, 255, 255), tag=(tag+2))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Tag Position: ")
                        dpg.add_text("0", tag=(tag+3))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Spawn Position: ")
                        dpg.add_text("0", tag=(tag+4))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Respawn Position: ")
                        dpg.add_text("0", tag=(tag+5))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Costume: ")
                        dpg.add_text("0", tag=(tag+6))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Tint: ")
                        dpg.add_text("0", tag=(tag+7))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Team: ")
                        dpg.add_text("0", tag=(tag+8))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Percent: ")
                        dpg.add_text("0", tag=(tag+18))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"SD's: ")
                        dpg.add_text("0", tag=(tag+24))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"Attack Count: ")
                        dpg.add_text("0", tag=(tag+37))

                with dpg.table_row():
                    with dpg.group(horizontal=True, horizontal_spacing=10):
                        dpg.add_text(f"GOBJ: ")
                        dpg.add_text("0xFEE1DEAD", tag=(tag+33))
                        dpg.add_button(label="copy", callback=lambda:dpg.set_clipboard_text(dpg.get_value(tag+33)))
