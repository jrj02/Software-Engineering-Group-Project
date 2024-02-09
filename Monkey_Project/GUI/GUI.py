from PyQt5.QtWidgets import *
from ui_GUI import Ui_MainWindow
from handlers.HandleFileOperations import FileHandler
# from PyQt5.QtCore import Qt
# import csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_handler = FileHandler()

        self.ui.icon_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

        # Connections
        self.ui.add_folder_btn.clicked.connect(self.file_handler.add_video_files)
        self.ui.export_file_btn.clicked.connect(self.file_handler.export_files_to_csv)
        # self.ui.view_data_btn.clicked.connect(self.display_csv) # TODO not implemented

    # Change checkable status of push buttons when stacked widget changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_widget.findChildren(QPushButton) \
                   + self.ui.full_menu_widget.findChildren(QPushButton)

        for btn in btn_list:
            if index in [4, 5]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    def load_csv(self):
        # Open a file dialog to select the CSV file
        csv_file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        '''
        if csv_file_path:
            # Call the method to load and display the CSV content
            self.display_csv(csv_file_path)
        '''

    # Functions for changing menu page
    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def on_process_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_process_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_data_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_data_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_help_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_help_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)


# if there's an error with qss, copy your relative path to qss file and paste it in "open" brackets

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    with open("styles/style.qss", "r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
