from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidget, QDesktopWidget, QTableWidgetItem, QHBoxLayout, QFrame
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

        video_player = QPushButton('Video Player here')
        video_player.setFixedSize(700, 500)

        rectangle_frame = QFrame()
        rectangle_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        rectangle_frame.setStyleSheet("border: 2px solid gray;")  # Customize the style
        rectangle_frame.setFixedSize(300, 500)

        buttons_and_rectangle_layout = QHBoxLayout()
        buttons_and_rectangle_layout.addWidget(video_player)
        buttons_and_rectangle_layout.addWidget(rectangle_frame)
        buttons_and_rectangle_layout.setAlignment(Qt.AlignLeft)


        style = self.style()

        layout.addWidget(button_home)
        layout.addWidget(button_video_processing)
        layout.addWidget(button_saved_data)
        layout.addLayout(buttons_and_rectangle_layout)

        file_name_label = QLabel(" File name: ")
        
        file_path_label = QLabel(" File path: ")

        date_label = QLabel(" Date: ")

        size_label = QLabel(" Size (MB): ")

        file_status_label = QLabel(" File status: ")

        layout.addWidget(file_name_label)
        layout.addWidget(file_path_label)
        layout.addWidget(date_label)
        layout.addWidget(size_label)
        layout.addWidget(file_status_label)

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
