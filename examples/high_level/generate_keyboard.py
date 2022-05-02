from telefone.tools import Keyboard, Button

# Simplest way of generating keyboard is non-builder interface
# Use <.row()> to add row
# Use <.add(Button(...))> to add button to the last row
# Use <.dict()> to make keyboard sendable
KEYBOARD_STANDARD = Keyboard(resize_keyboard=True)
KEYBOARD_STANDARD.add(Button(text="Button 1"))
KEYBOARD_STANDARD.add(Button(text="Button 2"))
KEYBOARD_STANDARD.row()
KEYBOARD_STANDARD.add(Button(text="Button 3"))
KEYBOARD_STANDARD = KEYBOARD_STANDARD.get_markup()

# <.add()> and <.row()> methods return the instance of Keyboard,
# so you can use it as builder
KEYBOARD_WITH_BUILDER = (
    Keyboard(resize_keyboard=True)
    .add(Button(text="Button 1"))
    .add(Button(text="Button 2"))
    .row()
    .add(Button(text="Button 3"))
    .get_markup()
)

assert KEYBOARD_STANDARD == KEYBOARD_WITH_BUILDER