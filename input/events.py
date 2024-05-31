"""
IMPORTANT:
These only work on Windows
"""

import pyperclip
import keyboard, mouse
import time

def selected_hotkey_trigger(link):
	"""
	Collects already highlighted text by copying, then afterwards restoring the
	text previously stored in the clipboard
	"""
	clipboard_contents = pyperclip.paste()
	keyboard.send("ctrl+c")
	time.sleep(.1)
	highlighted_text = pyperclip.paste()
	highlighted_text = cleanup_results(highlighted_text)
	if highlighted_text == "":
		link.no_word_selected()
	else:
		link.new_word_received(highlighted_text)
	pyperclip.copy(clipboard_contents)

def select_hotkey_trigger(link):
	"""
	Awaits left-click, then selects word with double-click and returns the
	word that was selected
	"""
	#TODO: Check for no word selected
	#TODO: Check for word is same as word from clipboard (so no word selected)
	#TODO: Remove whitespace

	clipboard_contents = pyperclip.paste()
	link.loading_message_received("Select word...")
	mouse.wait()
	mouse.click()
	time.sleep(.1)
	keyboard.send("ctrl+c")
	time.sleep(.1)
	highlighted_text = pyperclip.paste()
	highlighted_text = cleanup_results(highlighted_text)
	if highlighted_text == "":
		link.no_word_selected()
	else:
		link.new_word_received(highlighted_text)
	pyperclip.copy(clipboard_contents)

def cleanup_results(results):
	results = results.strip()
	return results
   