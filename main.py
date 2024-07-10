from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QIcon, QFont, QCursor
from PyQt6.QtWidgets import (
	QApplication,
	QMainWindow,
	QLabel,
	QVBoxLayout,
	QHBoxLayout,
	QSizePolicy,
	QStackedWidget,
	QPushButton,
	QScrollArea,
	QCheckBox,
	QGroupBox,
	QComboBox,
	QSlider,
	QLineEdit,
	QSpinBox,
	QWidget
	)

import sys, json, os

import gettext

from input.KeyboardListener import HotkeyManager
from input.events import change_select_hotkey_trigger, change_selected_hotkey_trigger
from webscraping.Webscraper import Webscraper
from utils.exceptions import *

basedir = os.path.dirname(__file__)

supported_languages = {
	"en": gettext.translation("base", localedir="locales", languages=["en"]), 
	"de": gettext.translation("base", localedir="locales", languages=["de"]) # Add fallback=true
}

class MainWindow(QMainWindow):

	HSTRETCH_FOR_HEADER_LABEL = 3
	VSTRETCH_FOR_CONTENT = 3
	MAX_STRETCH = 400
	MIN_WIDTH = 200
	MAX_WIDTH = 1920
	MIN_HEIGHT = 300
	MAX_HEIGHT = 1080
	CONTENT_MARGIN = 18

	def __init__(self):
		super().__init__()
		self.setWindowTitle("dictionfairy")
		self.setWindowIcon(QIcon(os.path.join(basedir, "icon.ico")))
		self.window_size = [config["window-size"][0], config["window-size"][1]]
		if not (self.MIN_WIDTH <= self.window_size[0] <= self.MAX_WIDTH and self.MIN_HEIGHT <= self.window_size[1] <= self.MAX_HEIGHT):
			raise ConfigErrorException("window-size", f"window width must be between {self.MIN_WIDTH} and " +
				f"{self.MAX_WIDTH}, and height must be between {self.MIN_HEIGHT} and {self.MAX_HEIGHT}")
		self.setFixedSize(QSize(*self.window_size))
		self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

		self.HotkeyManager = HotkeyManager(config["grab-selected-hotkey"], config["select-and-grab-hotkey"], self)
		self.Webscraper = Webscraper(config["preferred-dictionary"])

		self.main_page = self.create_main_page()
		self.settings_page = self.create_settings_page()

		self.stacked_widget = QStackedWidget()
		self.stacked_widget.addWidget(self.main_page)
		self.stacked_widget.addWidget(self.settings_page)

		self.setCentralWidget(self.stacked_widget)

	def create_main_page(self):
		# Creates the main page with expected contents and results

		# Lays out vertical boxes for header and main content
		main_layout = QVBoxLayout()

		# Splits the top bar into two sections
		main_top_layout = QHBoxLayout()

		# The word currently being searched
		self.current_word_label = QLineEdit("dictionfairy", objectName="current-word-label")
		self.current_word_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
		self.current_word_label.setReadOnly(True)
		self.current_word_label.editingFinished.connect(self.current_word_edited)
		main_top_layout.addWidget(self.current_word_label, stretch=self.HSTRETCH_FOR_HEADER_LABEL)

		# Edit the searched word
		self.current_word_edit_button = QPushButton(QIcon("imgs/edit-button.svg"), None, None, objectName="current-word-edit-button")
		self.current_word_edit_button.clicked.connect(self.current_word_edit_button_pressed)
		self.current_word_edit_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		main_top_layout.addWidget(self.current_word_edit_button)

		# Settings button in top bar redirects to settings page
		main_settings_button = QPushButton(_("Settings"))
		main_settings_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
		main_settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
		main_settings_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		main_settings_button.setProperty("objectClass", "page-button")
		main_top_layout.addWidget(main_settings_button)

		# Adds the top bar to the main layout
		main_layout.addLayout(main_top_layout)

		# Main content of page; dictionary results
		self.main_content = QLabel(_("Welcome to dictionfairy. This is a placeholder definition:\nUse your hotkey to select a new word!"), objectName="main-content")
		self.main_content.setWordWrap(True)
		self.main_content.setAlignment(Qt.AlignmentFlag.AlignTop or Qt.AlignmentFlag.AlignLeft)
		self.main_content.setFixedSize(QSize(config["window-size"][0]-self.CONTENT_MARGIN, self.main_content.height()))
		main_scroll = QScrollArea(objectName="main-scroll-area")
		main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(1))
		main_scroll.setWidget(self.main_content)
		main_layout.addWidget(main_scroll, stretch=self.VSTRETCH_FOR_CONTENT)

		# Create and return widget for entire main page
		main_widget = QWidget(objectName="main-page")
		main_widget.setLayout(main_layout)
		main_widget.setProperty("objectClass", "page")
		return main_widget

	def create_settings_page(self):
		# Creates the settings page

		# Defines boxes for settings
		settings_layout = QVBoxLayout()

		# Splits header into two sections
		settings_top_layout = QHBoxLayout()

		settings_top_header = QLabel(_("Settings"), objectName="settings-header")
		settings_top_layout.addWidget(settings_top_header, stretch=self.HSTRETCH_FOR_HEADER_LABEL)

		# Redirects to main page
		settings_main_button = QPushButton(_("Back"), objectName="back-button")
		settings_main_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
		settings_main_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
		settings_main_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		settings_main_button.setProperty("objectClass", "page-button")
		settings_top_layout.addWidget(settings_main_button)

		# Adds top section to settings layout
		settings_layout.addLayout(settings_top_layout)

		# Group box for general settings
		general_settings_group = QGroupBox(_("General"), objectName="general-header")
		general_settings_group.setAlignment(Qt.AlignmentFlag.AlignTop)

		# Buttons to change both hotkeys
		change_selected_hotkey_box = QHBoxLayout()
		change_selected_hotkey_label = QLabel(_("Search highlighted: "), objectName="change-selected-hotkey-label")
		change_selected_hotkey_button = QPushButton(config["grab-selected-hotkey"], objectName="change-selected-hotkey-button")
		change_selected_hotkey_button.clicked.connect(lambda: change_selected_hotkey_trigger(self.HotkeyManager, change_selected_hotkey_button, config))
		change_selected_hotkey_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		change_selected_hotkey_button.setProperty("objectClass", "hotkey-button")
		change_selected_hotkey_box.addWidget(change_selected_hotkey_label)
		change_selected_hotkey_box.addWidget(change_selected_hotkey_button)
		change_select_hotkey_box = QHBoxLayout()
		change_select_hotkey_label = QLabel(_("Search on click: "), objectName="change-select-hotkey-label")
		change_select_hotkey_button = QPushButton(config["select-and-grab-hotkey"], objectName="change-select-hotkey-button")
		change_select_hotkey_button.clicked.connect(lambda: change_select_hotkey_trigger(self.HotkeyManager, change_select_hotkey_button, config))
		change_select_hotkey_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		change_select_hotkey_button.setProperty("objectClass", "hotkey-button")
		change_select_hotkey_box.addWidget(change_select_hotkey_label)
		change_select_hotkey_box.addWidget(change_select_hotkey_button)


		# Stay on top radio button
		stay_on_top_button = QCheckBox(_("Stay on top"), objectName="stay-on-top-button")
		stay_on_top_button.setChecked(config["stay-on-top"])
		stay_on_top_button.checkStateChanged.connect(self.stay_on_top_button_toggled)
		stay_on_top_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		# Dictionary selection dropdown
		preferred_dictionary_label = QLabel(_("Preferred dictionary"), objectName="preferred-dictionary-label")
		preferred_dictionary_dropdown = QComboBox(objectName="preferred-dictionary-dropdown")
		preferred_dictionary_dropdown.addItems([
			"dwds.de: de-de",
			"leo: de-en",
			"WordReference: fr-en"])
		preferred_dictionary_dropdown.setCurrentText(config["preferred-dictionary"])
		preferred_dictionary_dropdown.currentTextChanged.connect(self.preferred_dictionary_changed)
		preferred_dictionary_dropdown.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

		# Actual format for general settings
		general_settings_layout = QVBoxLayout()
		general_settings_layout.addLayout(change_selected_hotkey_box)
		general_settings_layout.addLayout(change_select_hotkey_box)
		general_settings_layout.addWidget(stay_on_top_button)
		general_settings_layout.addWidget(preferred_dictionary_label)
		general_settings_layout.addWidget(preferred_dictionary_dropdown)

		# Place general settings in the group box
		general_settings_group.setLayout(general_settings_layout)

		# Group box for display settings
		display_settings_group = QGroupBox(_("Display"), objectName="display-header")
		display_settings_group.setAlignment(Qt.AlignmentFlag.AlignTop)

		# Window size width and height spinboxes
		window_size_label = QLabel(_("Window size"), objectName="window-size-label")
		window_size_box = QHBoxLayout()
		window_size_w_label = QLabel("Width: ", objectName="window-size-width-label")
		window_size_w_label.setAlignment(Qt.AlignmentFlag.AlignRight)
		window_size_w_spinbox = QSpinBox(objectName="window-size-x-spinbox")
		window_size_w_spinbox.setMinimum(self.MIN_WIDTH)
		window_size_w_spinbox.setMaximum(self.MAX_WIDTH)
		window_size_w_spinbox.setSingleStep(40)
		window_size_w_spinbox.setValue(config["window-size"][0])
		window_size_w_spinbox.valueChanged.connect(self.window_size_w_changed)
		window_size_h_label = QLabel("Height: ", objectName="window-size-height-label")
		window_size_h_label.setAlignment(Qt.AlignmentFlag.AlignRight)
		window_size_h_spinbox = QSpinBox(objectName="window-size-height-spinbox")
		window_size_h_spinbox.setMinimum(self.MIN_HEIGHT)
		window_size_h_spinbox.setMaximum(self.MAX_HEIGHT)
		window_size_h_spinbox.setSingleStep(40)
		window_size_h_spinbox.setValue(config["window-size"][1])
		window_size_h_spinbox.valueChanged.connect(self.window_size_h_changed)
		window_size_box.addWidget(window_size_w_label)
		window_size_box.addWidget(window_size_w_spinbox)
		window_size_box.addWidget(window_size_h_label)
		window_size_box.addWidget(window_size_h_spinbox)
		window_size_box.addWidget(QLabel(), stretch=self.MAX_STRETCH)

		# Text size slider
		text_size_label = QLabel(_("Text size"), objectName="text-size-label")
		text_size_slider = QSlider(Qt.Orientation.Horizontal)
		text_size_slider.setMinimum(10)
		text_size_slider.setMaximum(36)
		text_size_slider.setValue(config["text-size"])
		text_size_slider.valueChanged.connect(self.text_size_changed)
		text_size_slider.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		text_size_slider.setFixedSize(QSize(160, 18))

		# Format for display settings
		display_settings_layout = QVBoxLayout()
		display_settings_layout.addWidget(window_size_label)
		display_settings_layout.addLayout(window_size_box)
		display_settings_layout.addWidget(text_size_label)
		display_settings_layout.addWidget(text_size_slider)

		# Put display settings in the group box
		display_settings_group.setLayout(display_settings_layout)

		# Filler box for proper proportions when expanded
		filler_box = QLabel()

		# Place all group boxes into the settings layout
		settings_layout.addWidget(general_settings_group)
		settings_layout.addWidget(display_settings_group)
		settings_layout.addWidget(filler_box, stretch=self.MAX_STRETCH)

		# Create and return widget for entire settings page
		settings_widget = QWidget(objectName="settings-page")
		settings_widget.setLayout(settings_layout)
		settings_widget.setProperty("objectClass", "page")
		return settings_widget

	def new_word_received(self, new_word):
		# Occurs when a hotkey is pressed to search a new word
		self.current_word_label.setText(new_word)
		self.main_content.setText(_("Loading..."))
		self.main_content.setText("• " + "\n• ".join(self.Webscraper.search_dict_for(new_word)))

	def current_word_edited(self):
		self.current_word_label.setReadOnly(1)
		new_word = self.current_word_label.text()
		self.new_word_received(new_word)

	def current_word_edit_button_pressed(self):
		if self.current_word_label.isReadOnly():
			self.current_word_label.setReadOnly(0)
			self.current_word_label.selectAll()
		else:
			self.current_word_label.setReadOnly(1)

	def loading_message_received(self, loading_message):
		# Occurs when a hotkey has been pressed, but a word has not been selected
		self.current_word_label.setText(loading_message)
		self.main_content.setText(_("Waiting for word selection..."))

	def no_word_selected(self):
		# Occurs when a word has been selected, but the word is empty
		self.current_word_label.setText(_("No word selected... Try again!"))
		self.main_content.setText(_("Waiting for word selection..."))

	def stay_on_top_button_toggled(self, checked):
		# Toggles between window locked to top and not
		config["stay-on-top"] = (checked == Qt.CheckState.Checked)
		if config["stay-on-top"]:
			self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
			self.show()
		else:
			self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
			self.show()

	def preferred_dictionary_changed(self, new_text):
		# Changes the dictionary used for the webscraper
		config["preferred-dictionary"] = new_text
		self.Webscraper.set_dictionary(new_text)

	def window_size_w_changed(self, new_width):
		# Changes the width of the window
		self.window_size[0] = new_width
		self.setFixedSize(QSize(*self.window_size))
		self.main_content.setFixedSize(QSize(new_width-self.CONTENT_MARGIN, self.main_content.height()))
		config["window-size"][0] = new_width

	def window_size_h_changed(self, new_height):
		# Changes the height of the window
		self.window_size[1] = new_height
		self.setFixedSize(QSize(*self.window_size))
		config["window-size"][1] = new_height

	def text_size_changed(self, new_size):
		config["text-size"] = new_size
		self.setStyleSheet("font-size: " + str(new_size) + "px")



if __name__ == "__main__":

	if not os.path.exists("config.json"):
		with open("config.json", "w") as config_file:
			config_file.write("""
				{
				    "language": "en",
				    "stay-on-top": true,
				    "window-size": [
				        240,
				        380
				    ],
				    "text-size": 12,
				    "grab-selected-hotkey": "ctrl+u",
				    "select-and-grab-hotkey": "ctrl+i",
				    "preferred-dictionary": "dwds.de: de-de",
				    "style": "default"
				}
				""")

	with open("config.json") as config_file:
		config = json.load(config_file)

	if config["language"] not in supported_languages.keys():
		raise InvalidLanguageException(config["language"])

	supported_languages[config["language"]].install()

	app = QApplication(sys.argv)

	try:
		with open(os.path.join(basedir, "styles/" + config["style"] + ".qss"), 'r') as core_stylesheet:
			style = core_stylesheet.read()
			app.setStyleSheet(style)
	except:
		raise InvalidStyleException(config["style"])

	window = MainWindow()
	window.show()

	window.setStyleSheet("font-size: " + str(config["text-size"]) + "px")

	app.exec()

	window.HotkeyManager.clear_all_hotkeys()

	window.Webscraper.driver.close()

	with open("config.json", "w") as config_file:
		json.dump(config, config_file, indent=4)