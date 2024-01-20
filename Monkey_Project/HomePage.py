from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import subprocess

class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Home Page')
        self.setGeometry(350, 100, 300, 200)

        layout = QVBoxLayout()

        button_home = QPushButton('Home')
        button_home.clicked.connect(self.show_home)

        button_video_processing = QPushButton('Video Processing')
        button_video_processing.clicked.connect(self.show_video_processing)

        button_saved_data = QPushButton('Saved Data')
        button_saved_data.clicked.connect(self.show_saved_data)

        layout.addWidget(button_home)
        layout.addWidget(button_video_processing)
        layout.addWidget(button_saved_data)

        instructions_label = QLabel("Instructions:\n\n"
                                    "1. Click 'Home' to go to the home page.\n"
                                    "2. Click 'Video Processing' to open the video player.\n"
                                    "3. Click 'Saved Data' to view saved data.")

        layout.addWidget(instructions_label)

        self.setLayout(layout)

    def show_home(self):
        print("Showing Home Page")

    def show_video_processing(self):
        print("Showing Video Processing Page")
        subprocess.run(["python", "VideoPlayer.py"])

    def show_saved_data(self):
        print("Showing Saved Data Page")

if __name__ == "__main__":
    app = QApplication([])
    home_page = HomePage()
    home_page.show()
    app.exec_()
