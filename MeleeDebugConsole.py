import dearpygui.dearpygui as dpg
from melee_common import *
import threading
import time
import pm_common

clr_active = (91, 68, 50)
clr_click = (128, 95, 70)
clr_hover = (128, 95, 70)

title_bar_drag = False


def drag_viewport(sender, app_data, user_data):
    drag_deltas = app_data
    viewport_current_pos = dpg.get_viewport_pos()
    new_x_position = viewport_current_pos[0] + drag_deltas[1]
    new_y_position = viewport_current_pos[1] + drag_deltas[2]
    new_y_position = max(new_y_position, 0)  # prevent the viewport to go off the top of the screen
    dpg.set_viewport_pos([new_x_position, new_y_position])



def popup():
    if not dpg.does_item_exist("error_popup"):
        if dpg.does_item_exist("main_window"):
            with dpg.mutex():
                with dpg.window(tag="error_popup", width=330, height=150, show=True, no_title_bar=True,
                                modal=True, no_resize=True, no_close=True, no_move=True) as er_win:
                    _width = dpg.get_item_width(er_win)
                    _height = dpg.get_item_height(er_win)
                    dpg.add_text('Waiting for Dolphin.', tag="txt", pos=[90, 70])


def check_pm():
    # time.sleep(2)
    pm_common.resources_initialized.wait()
    while True:
        # print("\n\nstart")
        # print("pm: ", pm_common.pm)
        if pm_common.pm is None:
            # print("1")
            if dpg.does_item_exist("error_popup"):
                dpg.show_item("error_popup")
                waiting_dolphin()
                # print("2")
        elif pm_common.pm and dpg.does_item_exist("error_popup"):
            # print("3")
            if pm_common.GALE01 is None:
                dpg.show_item("error_popup")
                waiting_melee()
                # print("4")
            else:
                # print("GALE01: ", pm_common.GALE01)
                dpg.hide_item("error_popup")
                # print("5")
        time.sleep(1)


pm_thread = threading.Thread(target=pm_common.get_proc)
check_thread = threading.Thread(target=check_pm)

pm_thread.start()
check_thread.start()


def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)


def melee_debug_callback(sender, state):
    callback = callbacks.get(sender)
    if callback:
        callback(state, pm_common.pm, pm_common.GALE01)


def button_callback(sender, app_data, user_data):
    state, enabled_theme, disabled_theme = user_data
    state = not state
    dpg.bind_item_theme(sender, enabled_theme if state is True else disabled_theme)
    dpg.set_item_user_data(sender, (state, enabled_theme, disabled_theme))
    melee_debug_callback(sender, state)
    # print(sender)

    if sender == BTN_CVIS or BTN_CBBL:
        for player in player_overlays:
            value = 1 if state else 0
            dpg.set_value(player, value)
            for slider in player_overlays:
                dpg.configure_item(slider, enabled=state)


def colour_callback(sender, user_data):
    colour_int = [int(c * 255) for c in user_data]
    hex_colour = [hex(c)[2:].zfill(2) for c in colour_int][:3]
    update_bg_colour(hex_colour, pm_common.pm, pm_common.GALE01)


def slider_cb(sender, user_data):
    player = player_overlays.index(sender)
    byte = user_data
    print(player)
    collision_overlay(player, byte, pm_common.pm, pm_common.GALE01)


def exit_window():
    # dpg.destroy_context()
    pass

# def auto_align(item, alignment_type: int, x_align: float = 0.5, y_align: float = 0.5):
#     def _center_h(_s, _d, data):
#         parent = dpg.get_item_parent(data[0])
#         while dpg.get_item_info(parent)['type'] != "mvAppItemType::mvWindowAppItem":
#             parent = dpg.get_item_parent(parent)
#         parentWidth = dpg.get_item_rect_size(parent)[0]
#         width = dpg.get_item_rect_size(data[0])[0]
#         newX = (parentWidth // 2 - width // 2) * data[1] * 2
#         dpg.set_item_pos(data[0], [newX, dpg.get_item_pos(data[0])[1]])
#
#     def _center_v(_s, _d, data):
#         parent = dpg.get_item_parent(data[0])
#         while dpg.get_item_info(parent)['type'] != "mvAppItemType::mvWindowAppItem":
#             parent = dpg.get_item_parent(parent)
#         parentWidth = dpg.get_item_rect_size(parent)[1]
#         height = dpg.get_item_rect_size(data[0])[1]
#         newY = (parentWidth // 2 - height // 2) * data[1] * 2
#         dpg.set_item_pos(data[0], [dpg.get_item_pos(data[0])[0], newY])
#
#     if 0 <= alignment_type <= 2:
#         with dpg.item_handler_registry():
#             if alignment_type == 0:
#                 # horizontal only alignment
#                 dpg.add_item_visible_handler(callback=_center_h, user_data=[item, x_align])
#             elif alignment_type == 1:
#                 # vertical only alignment
#                 dpg.add_item_visible_handler(callback=_center_v, user_data=[item, y_align])
#             elif alignment_type == 2:
#                 # both horizontal and vertical alignment
#                 dpg.add_item_visible_handler(callback=_center_h, user_data=[item, x_align])
#                 dpg.add_item_visible_handler(callback=_center_v, user_data=[item, y_align])
#
#         dpg.bind_item_handler_registry(item, dpg.last_container())


def waiting_dolphin():
    if not dpg.does_item_exist("error_popup"):
        return
    text = dpg.get_value("txt")
    waiting_states = ["Waiting for Dolphin.", "Waiting for Dolphin..", "Waiting for Dolphin..."]
    if text in waiting_states:
        next_state = waiting_states[(waiting_states.index(text) + 1) % len(waiting_states)]
    else:
        next_state = "Waiting for Dolphin."
    dpg.set_value("txt", next_state)


def waiting_melee():
    if not dpg.does_item_exist("error_popup"):
        return
    text = dpg.get_value("txt")
    waiting_states = ["Waiting for Melee.", "Waiting for Melee..", "Waiting for Melee..."]
    if text in waiting_states:
        next_state = waiting_states[(waiting_states.index(text) + 1) % len(waiting_states)]
    else:
        next_state = "Waiting for Melee."
    dpg.set_value("txt", next_state)


################################
#         Window Start         #
################################
def main():
    width = 400
    height = 600
    dpg.create_context()
    dpg.create_viewport(title="Melee Debug Console", width=width, height=height, decorated=False, resizable=False)
    # dpg.setup_dearpygui()

    with dpg.window(label="Melee Debug Console", width=width, height=height, no_collapse=True, no_move=True, no_resize=True,
                    on_close=exit_window, tag="main_window"):

        with dpg.handler_registry():
            dpg.add_mouse_drag_handler(button=1, threshold=0.0, callback=drag_viewport)

        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, clr_active, category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 2, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, clr_active, category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, clr_click, category=dpg.mvThemeCat_Core)

            with dpg.theme_component(dpg.mvInputInt):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (140, 255, 23, 255), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

        dpg.bind_theme(global_theme)

        with dpg.theme() as disabled_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (51, 51, 57, 255), category=dpg.mvThemeCat_Core)

        with dpg.theme() as enabled_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (91, 68, 50, 255), category=dpg.mvThemeCat_Core)
        dpg.add_spacer(height=1)

        ################################
        #       In-Game Toggles        #
        ################################
        dpg.add_text("In-Game Toggles")
        _help("Various toggles")
        ingame_window = dpg.add_child_window(width=-1, height=94, autosize_x=True, no_scrollbar=True)
        with dpg.table(header_row=False, resizable=False, tag="ingame",
                       borders_outerH=False, borders_innerH=False,
                       borders_outerV=False, delay_search=True, parent=ingame_window):
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row(parent="ingame"):
                dpg.add_button(label="Pause", width=-1, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme), tag=150)

                dpg.add_button(label="HUD", width=-1, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme), tag=151)

                dpg.add_button(label="Particles & FX", width=-1, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme), tag=152)

            with dpg.table_row(parent="ingame"):
                dpg.add_button(label="Frame Advance", width=-1)

        ################################
        #            Stage             #
        ################################
        dpg.add_text("Stage")
        _help("'Visuals' displays stage structure, \n ECB's, ledge grab boxes, and more")
        stage_window = dpg.add_child_window(width=-1, height=122, autosize_x=True, no_scrollbar=True)
        with dpg.table(header_row=False, resizable=False, tag="stage_table",
                       borders_outerH=False, borders_innerH=False,
                       borders_outerV=False, delay_search=True, parent=stage_window):
        #
            dpg.add_table_column()
            dpg.add_table_column()
        #
            with dpg.table_row(parent="stage_table"):
                dpg.add_button(label="Visibility", width=-1, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme), tag=160)

                dpg.add_button(label="Visuals", width=-1, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme), tag=161)
            dpg.add_spacer(height=1, parent=stage_window)
            background_window = dpg.add_child_window(width=-1, height=40, autosize_x=True, parent=stage_window)

            with dpg.theme() as item_theme:
                with dpg.theme_component(dpg.mvAll):
                    dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (51, 51, 57, 255), category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 2, category=dpg.mvThemeCat_Core)
                    dpg.add_theme_style(dpg.mvStyleVar_ChildBorderSize, 1, category=dpg.mvThemeCat_Core)

            dpg.bind_item_theme(background_window, item_theme)
            with dpg.table(header_row=False, resizable=False, tag="bg_table",
                           borders_outerH=False, borders_innerH=False,
                           borders_outerV=False, delay_search=True, parent=background_window, height=-1):

                dpg.add_table_column()
                dpg.add_table_column()

                with dpg.table_row(parent="bg_table"):
                    dpg.add_text("Background Colour: ")
                    color = dpg.add_color_edit((0, 0, 0), no_label=True, width=-1, callback=colour_callback,
                                               user_data=True, display_mode=dpg.mvColorEdit_hex, no_alpha=True)
        dpg.add_spacer(height=10)

        ################################
        #          Characters          #
        ################################
        dpg.add_text("Characters")
        _help("Change character visibility and overlay modes.")
        character_window = dpg.add_child_window(width=-1, height=180, autosize_x=True)
        with dpg.table(header_row=False, resizable=False, tag="char_table",
                       borders_outerH=False, borders_innerH=False,
                       borders_outerV=False, delay_search=True, parent=character_window):

            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row(parent="char_table"):
                dpg.add_button(label="Hide", width=-1, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme), tag=170)

                dpg.add_button(label="Collision Bubbles", width=-1, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme), tag=171)

                sliders_window = dpg.add_child_window(width=-1, height=100, autosize_x=True, parent=character_window)
                with dpg.tab_bar(parent=sliders_window) as tab_bar:
                    for i in range(4):
                        with dpg.tab(label=f"Player {i + 1}", tag=f"tab_{i}"):
                            with dpg.group(horizontal=True):
                                dpg.add_text("Overlay Mode:")
                                dpg.add_slider_int(width=-1, max_value=3, tag=f"slider_{i}", callback=slider_cb,
                                                   default_value=1)
        # init alert
        popup()

    dpg.create_viewport(title="Melee Debug Console", width=width, height=height, decorated=False, resizable=False)
    dpg.show_viewport()
    dpg.setup_dearpygui()
    dpg.start_dearpygui()


if __name__ == "__main__":
    main()


