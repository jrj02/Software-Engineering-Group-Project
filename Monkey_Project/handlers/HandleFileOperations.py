import csv

from PyQt5.QtWidgets import QFileDialog


class FileHandler:

    # TODO Try to make this more dynamic if required
    @staticmethod
    def add_video_files():
        files = QFileDialog.getOpenFileNames(
            None,
            caption='Add trap videos to the app',  # set popup window title
            directory=':\\',  # resume from last directory
            filter='Supported Format (*.avi;*.mp4)'
        )
        if files:
            print(files)

    @staticmethod
    def export_files_to_csv():
        # TODO finish this function
        data = []

        # Code for debugging
        print(data)

        filename, _ = QFileDialog.getSaveFileName(None, 'Save File', '','CSV Files (*.csv)')
        if filename:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
