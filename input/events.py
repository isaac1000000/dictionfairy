import pyperclip
import keyboard, mouse
import time

def selected_hotkey_trigger(link):
	"""
	Collects already highlighted text by copying, then afterwards restoring the
	text previously stored in the clipboard
	"""
	keyboard.stash_state() # Workaround to stuck hotkeys, just clears all pressed keys
	clipboard_contents = pyperclip.paste()
	pyperclip.copy("") # Ensures that a word is copied
	keyboard.send("ctrl+c")
	time.sleep(.1)
	highlighted_text = cleanup_results(pyperclip.paste())
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
	keyboard.stash_state()  # Workaround to stuck hotkeys, just clears all pressed keys
	clipboard_contents = pyperclip.paste()
	pyperclip.copy("") # Ensures that a word is copied
	link.loading_message_received("Select word...")
	mouse.wait()
	mouse.click()
	time.sleep(.1)
	keyboard.send("ctrl+c")
	time.sleep(.1)
	highlighted_text = cleanup_results(pyperclip.paste())
	if highlighted_text == "":
		link.no_word_selected()
	else:
		link.new_word_received(highlighted_text)
	pyperclip.copy(clipboard_contents)

def cleanup_results(results):
	# TODO: Handle dashes for words on linebreaks? Might cause issues with french entries
	results = results.strip()
	return results
   
def change_select_hotkey_trigger(hotkey_manager, button, config_write):
	"""
	Waits for hotkey from keyboard, then sets the select hotkey in the hotkey manager to
	whatever was returned. Also sets the text of the relevant button and writes to the config file
	"""
	new_hotkey = keyboard.read_hotkey()
	hotkey_manager.set_select_and_grab_hotkey(new_hotkey)
	button.setText(new_hotkey)
	config_write["select-and-grab-hotkey"] = new_hotkey

def change_selected_hotkey_trigger(hotkey_manager, button, config_write):
	"""
	Waits for hotkey from keybaord, then sets the selected hotkey in the hotkey manager to
	whatever was returned. Also sets the text of the relevant button and writes to the config file
	"""
	new_hotkey = keyboard.read_hotkey()
	hotkey_manager.set_grab_selected_hotkey(new_hotkey)
	button.setText(new_hotkey)
	config_write["select-and-grab-hotkey"] = new_hotkey

