from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidget, QDesktopWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

import subprocess

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Home Page')

        self.resize(1000, 800)

        self.center_on_screen()

        layout = QVBoxLayout()

        button_home = QPushButton('Home')
        button_home.clicked.connect(self.show_home)

        button_video_processing = QPushButton('Video Processing')
        button_video_processing.clicked.connect(self.show_video_processing)

        button_saved_data = QPushButton('Saved Data')
        button_saved_data.clicked.connect(self.show_saved_data)

        button_add_folder = QPushButton('Add Folder')
        button_add_folder.clicked.connect(self.add_folder)
        button_add_folder.setFixedSize(120, 40)

        style = self.style()
        add_folder_icon = style.standardIcon(style.SP_FileDialogNewFolder)
        button_add_folder.setIcon(add_folder_icon)
        button_add_folder.setIconSize(QSize(24, 24))

        button_export = QPushButton('Export')
        button_export.clicked.connect(self.export)
        button_export.setFixedSize(120, 40)

        export_icon = style.standardIcon(style.SP_DialogSaveButton)
        button_export.setIcon(export_icon)
        button_export.setIconSize(QSize(24, 24))

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(button_add_folder)
        horizontal_layout.addWidget(button_export)
        horizontal_layout.setAlignment(Qt.AlignLeft)

        layout.addWidget(button_home)
        layout.addWidget(button_video_processing)
        layout.addWidget(button_saved_data)
        layout.addLayout(horizontal_layout)

        table = QTableWidget(self)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["File Name", "Videos inside", "Status"])
        

        layout.addWidget(table)

        instructions_label = QLabel("Instructions:\n\n"
                                    "1. Click 'Home' to go to the home page.\n"
                                    "2. Click 'Video Processing' to open the video player.\n"
                                    "3. Click 'Saved Data' to view saved data.")

        layout.addWidget(instructions_label)

        buttons_vertical_layout = QVBoxLayout()

        button_help = QPushButton('Help')
        button_help.setFixedSize(120, 30)
        buttons_vertical_layout.addWidget(button_help)

        help_button_icon = style.standardIcon(style.SP_TitleBarContextHelpButton)
        button_help.setIcon(help_button_icon)
        button_help.setIconSize(QSize(16, 16))

        button_exit = QPushButton('Exit')
        button_exit.setFixedSize(120, 30)
        buttons_vertical_layout.addWidget(button_exit)

        buttons_vertical_layout.setAlignment(Qt.AlignRight)

        layout.addLayout(buttons_vertical_layout)

        self.setLayout(layout)

    def center_on_screen(self):
        screen_geometry = QDesktopWidget().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def show_home(self):
        print("Showing Home Page")

    def show_video_processing(self):
        print("Showing Video Processing Page")
        subprocess.run(["python", "VideoPlayer.py"])

    def show_saved_data(self):
        print("Showing Saved Data Page")

    def add_folder(self):
        print("Add Folder")

    def export(self):
        print("Choose where to export file")

    def help(self):
        print("Help")
    
    def exit(self):
        print("Exit")

if __name__ == "__main__":
    app = QApplication([])
    home_page = HomePage()
    home_page.show()
    app.exec_()
