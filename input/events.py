"""
IMPORTANT:
These only work on Windows
"""

import pyperclip
import keyboard, mouse
import time

def selected_hotkey_trigger():
	"""
	Collects already highlighted text by copying, then afterwards restoring the
	text previously stored in the clipboard
	"""
	clipboard_contents = pyperclip.paste()
	keyboard.send("ctrl+c")
	time.sleep(.1)
	highlighted_text = pyperclip.paste()
	pyperclip.copy(clipboard_contents)
	print(highlighted_text)

def select_hotkey_trigger():
	"""
	Awaits left-click, then selects word with double-click and returns the
	word that was selected
	"""
	clipboard_contents = pyperclip.paste()
	mouse.double_click()
	time.sleep(.1)
	keyboard.send("ctrl+c")
	time.sleep(.1)
	highlighted_text = pyperclip.paste()
	pyperclip.copy(clipboard_contents)
	print(highlighted_text)

	