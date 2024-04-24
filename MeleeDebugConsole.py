import dearpygui.dearpygui as dpg
import dearpygui_extend as dpge

width = 400
height = 600

title_bar_drag = False

# layout = '''
# LAYOUT example center center
# 	COL left_menu 0.2
# 	COL
# 		ROW 0.3
# 			COL left_content
# 			COL right_content
# 		ROW
# 			COL bottom_content
# 	COL right_menu 0.2
# '''
#
# with dpg.window():
#     dpge.add_layout(layout, border=True)


def button_callback(sender, app_data, user_data):
    # Unpack the user_data that is currently associated with the button
    state, enabled_theme, disabled_theme = user_data
    # Flip the state
    state = not state
    # Apply the appropriate theme
    dpg.bind_item_theme(sender, enabled_theme if state is True else disabled_theme)
    # Update the user_data associated with the button
    dpg.set_item_user_data(sender, (state, enabled_theme, disabled_theme,))


def exit():
    dpg.destroy_context()


dpg.create_context()
viewport = dpg.create_viewport(title="w", width=width, height=height, decorated=False, resizable=False)
dpg.setup_dearpygui()

with dpg.window(label="Melee Debug Console", width=width, height=height, no_collapse=True, no_move=True, no_resize=True,
                on_close=exit) as win:
    with dpg.theme() as disabled_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (51, 51, 57, 255), category=dpg.mvThemeCat_Core)

    with dpg.theme() as enabled_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (34, 83, 118, 255), category=dpg.mvThemeCat_Core)

    with dpg.collapsing_header(label="In-Game Toggles", default_open=True, leaf=True):
        with dpg.group(horizontal=False):
            with dpg.group(horizontal=True, horizontal_spacing=10):
                dpg.add_spacer()
                dpg.add_button(label="Pause", width=50, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme))
                dpg.add_button(label="HUD", width=50, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme))
                dpg.add_button(label="Particles & FX", width=50, height=50, callback=button_callback,
                               user_data=(True, disabled_theme, enabled_theme))
                dpg.add_spacer()

def cal_dow(sender, data):
    global title_bar_drag
    if dpg.is_mouse_button_down(0):
        x = data[0]
        y = data[1]
        if -2 <= y <= 19:
            title_bar_drag = True
        else:
            title_bar_drag = False


def cal(sender, data):
    global title_bar_drag
    if title_bar_drag:
        pos = dpg.get_viewport_pos()
        x = data[1]
        y = data[2]
        final_x = pos[0] + x
        final_y = pos[1] + y
        dpg.configure_viewport(viewport, x_pos=final_x, y_pos=final_y)


with dpg.handler_registry():
    dpg.add_mouse_drag_handler(0, callback=cal)
    dpg.add_mouse_move_handler(callback=cal_dow)

dpg.show_viewport()
dpg.start_dearpygui()
