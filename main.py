from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
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
	QRadioButton,
	QGroupBox,
	QComboBox,
	QWidget
	)

import sys, json

from input.KeyboardListener import HotkeyManager
from webscraping.Webscraper import Webscraper

with open("config.json") as config_file:
	config = json.load(config_file)

class MainWindow(QMainWindow):

	HSTRETCH_FOR_HEADER_LABEL = 3
	VSTRETCH_FOR_CONTENT = 3
	SCROLL_BAR_WIDTH = 2

	def __init__(self):
		super().__init__()
		self.setWindowTitle("dictionfairy")
		self.setFixedSize(QSize(config["window-size"][0], config["window-size"][1]))
		self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, config["stay-on-top"])

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
		self.current_word_label = QLabel("dictionfairy")
		main_top_layout.addWidget(self.current_word_label, stretch=self.HSTRETCH_FOR_HEADER_LABEL)

		# Settings button in top bar redirects to settings page
		main_settings_button = QPushButton("Settings")
		main_settings_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
		main_settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
		main_top_layout.addWidget(main_settings_button)

		# Adds the top bar to the main layout
		main_layout.addLayout(main_top_layout)

		# Main content of page; dictionary results
		self.main_content = QLabel("Welcome to dictionfairy. This is a placeholder definition:\nUse your hotkey to select a new word!")
		self.main_content.setWordWrap(True)
		self.main_content.setAlignment(Qt.AlignmentFlag.AlignTop or Qt.AlignmentFlag.AlignLeft)
		self.main_content.setMaximumWidth(182) # Hardcoded for now, come back later to make dynamic
		main_scroll = QScrollArea()
		main_scroll.verticalScrollBar().setStyleSheet("QScrollBar {width:" + str(self.SCROLL_BAR_WIDTH)  + "px;}")
		main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy(1))
		main_scroll.setWidget(self.main_content)
		main_layout.addWidget(main_scroll, stretch=self.VSTRETCH_FOR_CONTENT)

		# Create and return widget for entire main page
		main_widget = QWidget()
		main_widget.setLayout(main_layout)
		return main_widget

	def create_settings_page(self):
		# Creates the settings page

		# Defines boxes for settings
		settings_layout = QVBoxLayout()

		# Splits header into two sections
		settings_top_layout = QHBoxLayout()

		settings_top_layout.addWidget(QLabel("Settings"), stretch=self.HSTRETCH_FOR_HEADER_LABEL)

		# Redirects to main page
		settings_main_button = QPushButton("Main")
		settings_main_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
		settings_main_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
		settings_top_layout.addWidget(settings_main_button)

		# Adds top section to settings layout
		settings_layout.addLayout(settings_top_layout)

		# Group box for general settings
		general_settings_group = QGroupBox("General")
		general_settings_group.setAlignment(Qt.AlignmentFlag.AlignTop)

		# Stay on top radio button
		stay_on_top_button = QRadioButton("Stay on top")

		# Dictionary selection dropdown
		preferred_dictionary_label = QLabel("Preferred dictionary")
		preferred_dictionary_dropdown = QComboBox()
		preferred_dictionary_dropdown.addItems([
			"DWDS",
			"Leo",
			"Merriam-Webster"])

		# Actual format for general settings
		general_settings_layout = QVBoxLayout()
		general_settings_layout.addWidget(stay_on_top_button)
		general_settings_layout.addWidget(preferred_dictionary_label)
		general_settings_layout.addWidget(preferred_dictionary_dropdown)

		# Place general settings in the group box
		general_settings_group.setLayout(general_settings_layout)

		# Group box for display settings
		display_settings_group = QGroupBox("Display")
		display_settings_group.setAlignment(Qt.AlignmentFlag.AlignTop)

		# Window size dropdown
		window_size_label = QLabel("Window size")
		window_size_dropdown = QComboBox()
		window_size_dropdown.addItems([
			"200, 300",
			"2000, 3000",
			"10123123, 90187612983471293847"])

		# Text size dropdown
		text_size_label = QLabel("Text size")
		text_size_dropdown = QComboBox()
		text_size_dropdown.addItems([
			"10",
			"12",
			"13"])

		# Format for display settings
		display_settings_layout = QVBoxLayout()
		display_settings_layout.addWidget(window_size_label)
		display_settings_layout.addWidget(window_size_dropdown)
		display_settings_layout.addWidget(text_size_label)
		display_settings_layout.addWidget(text_size_dropdown)

		# Put display settings in the group box
		display_settings_group.setLayout(display_settings_layout)

		# Place all group boxes into the settings layout
		settings_layout.addWidget(general_settings_group)
		settings_layout.addWidget(display_settings_group)

		# Create and return widget for entire settings page
		settings_widget = QWidget()
		settings_widget.setLayout(settings_layout)
		return settings_widget

	def new_word_received(self, new_word):
		# Occurs when a hotkey is pressed to search a new word
		self.current_word_label.setText(new_word)
		self.main_content.setText("\n".join(self.Webscraper.search_dict_for(new_word)))

if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	app.exec()

with open("config.json", "w") as config_file:
	json.dump(config, config_file, indent=4)