import time
import vgamepad as vg

from gamepad.gamepad_buttons import GamepadButtons
from controller_socket.controller_socket import ControllerSocket


gamepad = vg.VX360Gamepad()
gamepad_buttons = GamepadButtons()

# press a button to wake the device up
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(1)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(1)

ws = ControllerSocket()
ws.connect()

while True:
    gamepad_buttons.update_joystick_values(joystick_values=ws.js_values)
    gamepad_buttons.update_button_values(button_val=ws.switch_02)

    if gamepad_buttons.BUTTON_CHANGED:
        if ws.switch_02:
            gamepad.press_button(0x1000)
        else:
            gamepad.release_button(0x1000)
        gamepad_buttons.BUTTON_CHANGED = 0

    gamepad.left_joystick(x_value=gamepad_buttons.LJS_X, y_value=gamepad_buttons.LJS_Y)  # values between -32768 and 32767
    gamepad.right_joystick(x_value=gamepad_buttons.RJS_X, y_value=gamepad_buttons.RJS_Y)  # values between -32768 and 32767
    
    gamepad.update()
