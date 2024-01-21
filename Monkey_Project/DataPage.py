from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget


class DataPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Saved Data')
        self.setGeometry(350, 100, 400, 250)

        layout = QVBoxLayout()

        data_label = QLabel("Select the data sets you want to view:")
        layout.addWidget(data_label)

        self.data_set_list = QListWidget()
        self.set_data_sets([f"Data Set {i}" for i in range(1, 6)])  # placeholder
        layout.addWidget(self.data_set_list)

        self.setLayout(layout)

    # TODO Return selected dataset
    def get_selected_dataset(self):
        return None

    # TODO Takes in data_sets for this page
    def set_data_sets(self, data_sets):
        self.data_set_list.clear()
        for data_set in data_sets:
            self.data_set_list.addItem(data_set)


if __name__ == "__main__":
    app = QApplication([])
    data_page = DataPage()
    data_page.show()
    app.exec_()
