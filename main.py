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
	QWidget
	)

import sys, json

with open("config.json") as config_file:
	config = json.load(config_file)

HSTRETCH_FOR_HEADER_LABEL = 3
VSTRETCH_FOR_CONTENT = 3

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("dictionfairy")
		self.setFixedSize(QSize(config["window-size"][0], config["window-size"][1]))

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
		current_word = QLabel("SAMPLEWORD")
		main_top_layout.addWidget(current_word, stretch=HSTRETCH_FOR_HEADER_LABEL)

		# Settings button in top bar redirects to settings page
		main_settings_button = QPushButton("Settings")
		main_settings_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
		main_settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
		main_top_layout.addWidget(main_settings_button)

		# Adds the top bar to the main layout
		main_layout.addLayout(main_top_layout)

		# Main content of page; dictionary results
		main_content = QLabel("SAMPLERESULTS " * 100)
		main_content.setWordWrap(True)
		main_content.setAlignment(Qt.AlignmentFlag.AlignTop)
		main_content.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
		main_layout.addWidget(main_content, stretch=VSTRETCH_FOR_CONTENT)

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

		settings_top_layout.addWidget(QLabel("Settings"), stretch=HSTRETCH_FOR_HEADER_LABEL)

		# Redirects to main page
		settings_main_button = QPushButton("Main")
		settings_main_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
		settings_main_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
		settings_top_layout.addWidget(settings_main_button)

		# Adds top section to settings layout
		settings_layout.addLayout(settings_top_layout)

		# Samples settings
		setting1 = QLabel("SAMPLESETTING")
		setting1.setAlignment(Qt.AlignmentFlag.AlignLeft)
		setting1.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
		settings_layout.addWidget(setting1, stretch=VSTRETCH_FOR_CONTENT)

		# Create and return widget for entire settings page
		settings_widget = QWidget()
		settings_widget.setLayout(settings_layout)
		return settings_widget


if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = MainWindow()
	window.show()

	app.exec()

with open("config.json", "w") as config_file:
	json.dump(config, config_file, indent=4)