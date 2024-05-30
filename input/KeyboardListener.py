from input import events
import keyboard

class HotkeyManager():
	"""
	This class will listen to the user's keyboard for the intended input and 
	then trigger the appropriate event if the right hotkey combination
	is pressed
	"""
	def __init__(self, grab_selected_hotkey, select_and_grab_hotkey, link):
		self.grab_selected_hotkey = grab_selected_hotkey
		self.select_and_grab_hotkey = select_and_grab_hotkey
		self.link = link

		if grab_selected_hotkey != "":
			keyboard.add_hotkey(grab_selected_hotkey, events.selected_hotkey_trigger, args=[self.link], suppress=True, trigger_on_release=True)
			print(grab_selected_hotkey)
		if select_and_grab_hotkey != "":
			keyboard.add_hotkey(select_and_grab_hotkey, events.select_hotkey_trigger, args=[self.link], suppress=True)

	def clear_grab_selected_hotkey(self):
		keyboard.remove_hotkey(self.grab_selected_hotkey)

	def clear_select_and_grab_hotkey(self):
		keyboard.remove_hotkey(self.select_and_grab_hotkey)

	def clear_all_hotkeys(self):
		keyboard.unhook_all_hotkeys()

	def set_grab_selected_hotkey(self, target):
		self.clear_grab_selected_hotkey()
		self.grab_selected_hotkey = target
		add_hotkey(grab_selected_hotkey, events.selected_hotkey_trigger)

	def set_select_and_grab_hotkey(self, target):
		self.clear_select_and_grab_hotkey()
		self.select_and_grab_hotkey = target
		add_hotkey(select_and_grab_hotkey, events.select_hotkey_trigger)