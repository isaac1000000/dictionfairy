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
	if highlighted_text == clipboard_contents:
		link.no_word_selected()
		return
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
	clipboard_contents = pyperclip.paste()
	link.loading_message_received("Select word...")
	mouse.wait()
	mouse.click()
	time.sleep(.1)
	keyboard.send("ctrl+c")
	time.sleep(.1)
	highlighted_text = pyperclip.paste()
	if highlighted_text == clipboard_contents:
		link.no_word_selected()
		return
	highlighted_text = cleanup_results(highlighted_text)
	if highlighted_text == "":
		link.no_word_selected()
	else:
		link.new_word_received(highlighted_text)
	pyperclip.copy(clipboard_contents)

def cleanup_results(results):
	# TODO: Handle dashes for words on linebreaks? Might cause issues with french entries
	results = results.strip()
	return results
   