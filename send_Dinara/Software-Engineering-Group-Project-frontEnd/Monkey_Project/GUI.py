from PyQt5.QtWidgets import *
from ui_GUI import Ui_MainWindow
from location_window import RadioButtonListDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
import csv
import os
import json
from PyQt5 import QtWidgets, QtMultimedia, uic, QtCore
from PyQt5.QtCore import QDateTime
import subprocess
import threading
import atexit

file_info = "file_info.json"
#processed_file_info = "processed_file_info.json"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.refreshTableHome()

        self.ui.icon_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.home_btn_2.setChecked(True)

        # Connections
        self.ui.add_folder_btn.clicked.connect(self.add_files)
        self.ui.open_vid_btn.clicked.connect(self.open_file)
        self.ui.play_btn.clicked.connect(self.play_video)
        self.ui.browseButton.clicked.connect(self.browse_output_path)
        self.ui.export_file_btn.clicked.connect(self.export_files)

        #Create context menu for the tableWidget
        self.createContextMenu()

        # Add QMediaPlayer and QVideoWidget
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self.ui.widget_2)
        self.media_player.setVideoOutput(self.video_widget)
        self.video_widget.setObjectName("widget_2")
        self.video_widget.setAutoFillBackground(True)
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(r"C:\Users\rayev\Desktop\zamba_test\videos\poopossum_example_processed.AVI")))
        self.media_player.play()

        #Replay video when video ends
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        #Connect movement of the slider with video
        self.ui.horizontalSlider.sliderMoved.connect(self.set_position)

        #default output path
        self.ui.output_path_label.setText("C:\\Users\\rayev\\Desktop\\send_Dinara\\Software-Engineering-Group-Project-frontEnd\\Monkey_Project\\videos")

        # Register to clear JSON files on exit
        atexit.register(self.clear_json_files)


    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
    
    def handle_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0) 
            self.media_player.play()  

    def update_play_pause_button_icon(self):
        # Update the icon of the play/pause button based on the state of the media player
        if self.media_player.state() == QMediaPlayer.PlayingState:
            # Media player is playing, set the pause icon
            self.ui.play_btn.setIcon(QIcon("Software-Engineering-Group-Project-frontEnd\Monkey_Project\icon\pause-64.png"))
        else:
            # Media player is paused or stopped, set the play icon
            self.ui.play_btn.setIcon(QIcon("Software-Engineering-Group-Project-frontEnd\Monkey_Project\icon\play-64.png"))

    #set the position of the slider
    def position_changed(self, position):
        self.ui.horizontalSlider.setValue(position)

    #set the duration of the slider
    def duration_changed(self, duration):
        self.ui.horizontalSlider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)


    def open_file(self):
        default_folder = "Software-Engineering-Group-Project-frontEnd/processed_videos"
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video", default_folder)

        if filename != '':
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.media_player.play()

             # Update the file_name_lbl with the selected file name
            self.ui.file_name_lbl.setText(f"File Name: {os.path.basename(filename)}")

            # Update the file_path_lbl with the path of the selected file
            self.ui.file_path_lbl.setText(f"File Path: {filename}")

            # Get the file size in megabytes
            file_size_byte = os.path.getsize(filename)
            file_size_mb = file_size_byte / (1024 * 1024)

            # Update the size_lbl with the file size
            self.ui.size_lbl.setText(f"Size: {file_size_mb:.2f} MB")

            # Get the last modified time in a readable format
            last_modified_time = int(os.path.getmtime(filename))
            last_modified_date = QDateTime.fromSecsSinceEpoch(last_modified_time).toString("yyyy-MM-dd hh:mm:ss")

            # Update the date_lbl with the last modified date
            self.ui.date_lbl.setText(f"Last Modified: {last_modified_date}")

    def browse_output_path(self):
        new_output_path = QFileDialog.getExistingDirectory(self, "Select Output Path")

        if new_output_path:
            self.ui.output_path_label.setText(new_output_path)


    def createContextMenu(self):
        self.context_menu = QMenu(self)
        self.context_menu.addAction("Process Video (monkey presence)", self.process_video_monkey_presence)
        self.context_menu.addAction("Process Video (blank/non-blank)", self.process_video_blank_non_blank)

        self.ui.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.showContextMenu)

    def process_video_monkey_presence(self):
        selected_rows = set(index.row() for index in self.ui.tableWidget.selectionModel().selectedIndexes())
        new_output_path = self.ui.output_path_label.text()
        for row in selected_rows:
            file_name = self.ui.tableWidget.item(row, 0).text()
            file_directory = self.ui.tableWidget.item(row, 1).text()
            file_path = os.path.join(file_directory, file_name)

            print(f"Processing video (monkey presence) for: {file_path}")

            self.update_json_status(file_name, "Processing")
            self.refreshTableHome()

            thread = threading.Thread(target=self.process_video_thread_monkey_presence, args=(file_path,))
            thread.start()

    
    def process_video_blank_non_blank(self):
        selected_rows = set(index.row() for index in self.ui.tableWidget.selectionModel().selectedIndexes())
        new_output_path = self.ui.output_path_label.text()
        for row in selected_rows:
            file_name = self.ui.tableWidget.item(row, 0).text()
            file_directory = self.ui.tableWidget.item(row, 1).text()
            file_path = os.path.join(file_directory, file_name)

            print(f"Processing video (blank_non-blank) for: {file_path}")

            self.update_json_status(file_name, "Processing")
            self.refreshTableHome()

            thread = threading.Thread(target=self.process_video_thread_blank_nonblank, args=(file_path,))
            thread.start()

    
    def process_video_thread_monkey_presence(self, file_path):
        try:
            command = f"python yolov5/detect.py --weights yolov5/best.pt --source {file_path}"
            subprocess.run(command, shell=True)

            # Update list on data page that the video is done processing
            self.update_processed_list_widget()

            # Open and read the detection result JSON file
            with open('detection_result.json', 'r') as json_file:
                detection_result = json.load(json_file)
        
            # Check if detection status is "detection verified"
            if detection_result.get('detection_status') == 'detection verified':
                # Append detection results to file_info.json for the selected video
                with open(file_info, 'r+') as f:
                    data = json.load(f)
                    for category in data.values():
                        for file_data in category:
                            if file_data["file_name"] == os.path.basename(file_path):
                                file_data["detection_results"] = "Monkey detected"
                                break
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()

            # After processing, update status to "Processed" in the JSON data and refresh the table
            self.update_json_status(os.path.basename(file_path), "Processed")
            self.refreshTableHome()
            # Update list on data page that the video is done processing
            self.update_processed_list_widget()
        except Exception as e:
            print(f"Error processing video: {e}")
    
    
    def process_video_thread_blank_nonblank(self, file_path):
        try:
            command = f"python yolov5/detect.py --weights yolov5/best2.pt --source {file_path}"
            subprocess.run(command, shell=True)

            # After processing, update status to "Processed" in the JSON data and refresh the table
            self.update_json_status(os.path.basename(file_path), "Processed")
            self.refreshTableHome()

            #Update list on data page that the video is done processing
            self.update_processed_list_widget()
        except Exception as e:
            print(f"Error processing video: {e}")
            import traceback
            traceback.print_exc()


    def update_json_status(self, file_name, status):
        with open(file_info, 'r+') as f:
            data = json.load(f)
            for category in data.values():
                for file_data in category:
                    if file_data["file_name"] == file_name:
                        file_data["status"] = status

                        if status == "Processed":
                            # Load detection result from detection_result.json
                            with open('detection_result.json', 'r') as detection_file:
                                detection_result = json.load(detection_file)
                                detection_status = detection_result.get('detection_status', 'None')

                            if detection_result.get('detection_status') == 'detection verified':
                                 file_data["detection_results"] = "Monkey detected"

                            
                            processed_file_info = "processed_file_info.json"
                            if os.path.exists(processed_file_info):
                                with open(processed_file_info, "r") as processed_f:
                                    processed_data = json.load(processed_f)
                            else:
                                processed_data = {}

                            processed_data[file_name] = file_data
                            with open(processed_file_info, "w") as processed_f:
                                json.dump(processed_data, processed_f, indent=4)

                        break
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
        
    
    def update_processed_list_widget(self):
        self.ui.listWidget.clear()

        # Load processed file information from processed_file_info.json
        processed_file_info = "processed_file_info.json"
        if os.path.exists(processed_file_info):
            with open(processed_file_info, "r") as processed_f:
                processed_data = json.load(processed_f)
                for file_name in processed_data:
                    self.ui.listWidget.addItem(file_name)
        
        #Update the list to reflect changes
        self.ui.listWidget.update()

    
    def showContextMenu(self, position):
        self.context_menu.exec_(self.ui.tableWidget.mapToGlobal(position))


    # Change checkable status of pushbuttons when stackedwidget changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_widget.findChildren(QPushButton) \
                   + self.ui.full_menu_widget.findChildren(QPushButton)

        for btn in btn_list:
            if index in [4, 5]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    def add_files(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)")

        dialog = RadioButtonListDialog()
        

        if file_path:
            dialog = RadioButtonListDialog()
            dialog.exec_()
            selected_radio_button = dialog.get_selected_radio_buttons()  # Get selected radio button
            self.append_json(file_path, file_info, selected_radio_button)

    def append_json(self, file_path, file_info, selected_radio_button):

        data_all = {}

        if os.path.isfile(file_path) and (file_path.endswith(".AVI") or file_path.endswith(".mp4")):

            file_name = os.path.basename(file_path)
            file_size_byte = os.path.getsize(file_path)
            file_size_mb = file_size_byte/ (1024 * 1024)
            category_name = os.path.dirname(file_path)

            # Get the last modified time in a readable format
            last_modified_time = os.path.getmtime(file_path)
            last_modified_date = QDateTime.fromSecsSinceEpoch(last_modified_time).toString("yyyy-MM-dd hh:mm:ss")


            data_temp = {
                "file_name": file_name,
                "file_path": file_path,
                "file_size_mb": file_size_mb,
                "status": "Ready to Process",
                "location": selected_radio_button,
                "timestamp": last_modified_date,
                "detection_results": "None",
            }

            if category_name in data_all:
                data_all[category_name].append(data_temp)
            else:
                data_all[category_name] = [data_temp]
       
        if os.path.exists(file_info):
            with open(file_info, "r") as f:
                try:
                    existing_data_all = json.load(f)
                except ValueError:
                    existing_data_all = {}
        else:
            existing_data_all = {}

        for category_name, category_data in data_all.items():
            if category_name in existing_data_all:
                existing_data_all[category_name].extend(category_data)
            else:
                existing_data_all[category_name] = category_data
        
        with open(file_info, "w") as f:
            json.dump(existing_data_all, f, indent=4)

        self.refreshTableHome()



    def refreshTableHome(self):
        self.ui.tableWidget.clear()

        with open(file_info, 'r') as f:
            data = json.load(f)

        cat_List = list(data.keys())

        self.ui.tableWidget.setRowCount(len(cat_List))

        self.ui.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        item = QtWidgets.QTableWidgetItem("File Name")
        self.ui.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem("Directory")
        self.ui.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem("Status")
        self.ui.tableWidget.setHorizontalHeaderItem(2, item)

        for i, category in enumerate(cat_List):
            count = len(data[category])
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(category))

            for j, file_data in enumerate(data[category]):
            # Set the file name in the first column
                self.ui.tableWidget.setItem(i + j, 0, QtWidgets.QTableWidgetItem(file_data["file_name"]))
            # Set the directory in the second column
                self.ui.tableWidget.setItem(i + j, 1, QtWidgets.QTableWidgetItem(category))
            #Set the status in the third column
                self.ui.tableWidget.setItem(i + j, 2, QtWidgets.QTableWidgetItem(file_data["status"]))

    
    def export_files(self):
        processed_file_info = "processed_file_info.json"
        if os.path.exists(processed_file_info):
            excel_filename, _ = QFileDialog.getSaveFileName(self, "Export to Excel", "", "Excel Files (*.xlsx)")

            if excel_filename:
                try:
                    with open(processed_file_info, "r") as processed_f:
                        processed_data = json.load(processed_f)

                    with open(excel_filename, 'w', newline='', encoding='utf-8') as file:
                        fieldnames = ["File Name", "File Path", "File Size (MB)", "Status", "Time-stamp", "Location", "Detection result"]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        for file_name, file_data in processed_data.items():
                            writer.writerow({
                                "File Name": file_name,
                                "File Path": file_data["file_path"],
                                "File Size (MB)": file_data["file_size_mb"],
                                "Status": file_data["status"],
                                "Time-stamp": file_data["timestamp"],
                                "Location": file_data["location"],
                                "Detection result": file_data["detection_results"]
                            })

                    QtWidgets.QMessageBox.information(self, "Export Successful", "Data exported to Excel successfully.")
                except Exception as e:
                    QtWidgets.QMessageBox.critical(self, "Export Error", f"An error occurred: {str(e)}")
        else:
            QtWidgets.QMessageBox.warning(self, "No Data", "No processed data available to export.")

    
    def clear_json_files(self):
        # List of JSON files to clear
        json_files = ["file_info.json", "processed_file_info.json", "detection_result.json"]

        for json_file in json_files:
            try:
                # Truncate the file and write only the curly braces
                with open(json_file, 'w') as f:
                    f.write("{}")
            except Exception as e:
                print(f"Error clearing content of {json_file}: {e}")


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


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    with open("Software-Engineering-Group-Project-frontEnd\Monkey_Project\style.qss", "r") as style_file:
        style_str = style_file.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
