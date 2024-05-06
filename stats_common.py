import dearpygui.dearpygui as dpg

PLAYER_TAGS = []

# trust me, i didnt want to do this...
# string tags in dearpygui seem to be abl e to conflict with other flags...
# meaning at random, a "new" tag could replace or reference a different tag?
# this has lead me to creating tags in the thousands, so hopefully they never conflict with previous tags made.
for i in range(4):
    offset = i * 100
    playerblock_dict = {}
    playerblock_dict[offset + 8000] = "state"
    playerblock_dict[offset + 8001] = "ckind"
    playerblock_dict[offset + 8002] = "pkind"
    playerblock_dict[offset + 8003] = "tag_pos"
    playerblock_dict[offset + 8004] = "spawn_pos"
    playerblock_dict[offset + 8005] = "respawn_pos"
    playerblock_dict[offset + 8006] = "costume"
    playerblock_dict[offset + 8007] = "tint"
    playerblock_dict[offset + 8008] = "team"
    playerblock_dict[offset + 8009] = "controller"
    playerblock_dict[offset + 8010] = "cpu_lvl"
    playerblock_dict[offset + 8011] = "cpu_kind"
    playerblock_dict[offset + 8012] = "handicap"
    playerblock_dict[offset + 8013] = "kirby_copy"
    playerblock_dict[offset + 8014] = "attack"
    playerblock_dict[offset + 8015] = "kb"
    playerblock_dict[offset + 8016] = "defense"
    playerblock_dict[offset + 8017] = "scale"
    playerblock_dict[offset + 8018] = "damage"
    playerblock_dict[offset + 8019] = "initial_damage"
    playerblock_dict[offset + 8020] = "stamina"
    playerblock_dict[offset + 8021] = "falls"
    playerblock_dict[offset + 8022] = "ko"
    playerblock_dict[offset + 8023] = "x88"
    playerblock_dict[offset + 8024] = "self_destructs"
    playerblock_dict[offset + 8025] = "stocks"
    playerblock_dict[offset + 8026] = "coins_curr"
    playerblock_dict[offset + 8027] = "coins_total"
    playerblock_dict[offset + 8028] = "x98"
    playerblock_dict[offset + 8029] = "x9C"
    playerblock_dict[offset + 8030] = "stick_smashes"
    playerblock_dict[offset + 8031] = "tag"
    playerblock_dict[offset + 8032] = "xAC"
    playerblock_dict[offset + 8033] = "gobj"
    playerblock_dict[offset + 8034] = "sub_gobj"
    playerblock_dict[offset + 8035] = "callback"
    playerblock_dict[offset + 8036] = "stale_move"
    playerblock_dict[offset + 8037] = "atk_count"
    PLAYER_TAGS.append(playerblock_dict)


# for i in range(4):
#     offset = i * 100
#     gobj_dict = {}
#     gobj_dict[offset + 9000] = "entity_class"
#     gobj_dict[offset + 9001] = "p_link"
#     gobj_dict[offset + 9002] = "gx_link"
#     gobj_dict[offset + 9003] = "p_priority"
#     gobj_dict[offset + 9004] = "gx_pri"
#     gobj_dict[offset + 9005] = "obj_kind"
#     gobj_dict[offset + 9006] = "data_kind"
#     gobj_dict[offset + 9007] = "next"
#     gobj_dict[offset + 9008] = "previous"
#     gobj_dict[offset + 9009] = "nextOrdered"
#     gobj_dict[offset + 9010] = "previousOrdered"
#     gobj_dict[offset + 9011] = "proc"
#     gobj_dict[offset + 9012] = "gx_cb"
#     gobj_dict[offset + 9013] = "cobj_links"
#     gobj_dict[offset + 9014] = "hsd_object"
#     gobj_dict[offset + 9015] = "userdata"
#     gobj_dict[offset + 9016] = "destructor_function"
#     gobj_dict[offset + 9017] = "unk_linked_list"
#     PLAYER_GOBJS.append(gobj_dict)


def create_player_tables(window):
    s = 0
    with dpg.collapsing_header(label=f"Players", parent=window):
        for s in range(4):
            if s > 0:
                player_tag = 8000 + (s * 100)
                gobj_tag = 9000 + (s * 100)
            else:
                player_tag = 8000
                gobj_tag = 9000

            with dpg.tree_node(label=f"Port {s+1}"):
                with dpg.table(header_row=False, borders_innerH=False, borders_outerH=True,
                               borders_innerV=True, borders_outerV=True):
                    dpg.add_table_column()

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"State: ")
                            dpg.add_text("def", color=(255, 0, 0), tag=player_tag)

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Character: ")
                            dpg.add_text("def", color=(255, 0, 0), tag=(player_tag+1))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Slot Type: ")
                            dpg.add_text("def", color=(255, 255, 255), tag=(player_tag+2))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Tag Position: ")
                            dpg.add_text("0", tag=(player_tag+3))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Spawn Position: ")
                            dpg.add_text("0", tag=(player_tag+4))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Respawn Position: ")
                            dpg.add_text("0", tag=(player_tag+5))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Costume: ")
                            dpg.add_text("0", tag=(player_tag+6))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Tint: ")
                            dpg.add_text("0", tag=(player_tag+7))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Team: ")
                            dpg.add_text("0", tag=(player_tag+8))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Percent: ")
                            dpg.add_text("0", tag=(player_tag+18))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"SD's: ")
                            dpg.add_text("0", tag=(player_tag+24))

                    with dpg.table_row():
                        with dpg.group(horizontal=True, horizontal_spacing=10):
                            dpg.add_text(f"Attack Count: ")
                            dpg.add_text("0", tag=(player_tag+37))

                    with dpg.table_row():
                        with dpg.tree_node(label=f"GOBJ Data"):
                            with dpg.group(horizontal=True, horizontal_spacing=10):
                                dpg.add_text(f"GOBJ: ")
                                # dpg.add_text("0xFEE1DEAD", tag=(tag+33))
                                dpg.add_input_text(width=80, readonly=True, tag=(player_tag+33), callback=lambda:dpg.set_clipboard_text(dpg.get_value(player_tag+33)))
                                # dpg.add_input_text(width=80, readonly=True, tag=(tag+33), callback=lambda:dpg.set_clipboard_text(dpg.get_value(tag+33)))
                                dpg.add_button(label="copy", callback=lambda:dpg.set_clipboard_text(dpg.get_value(player_tag+33)))







