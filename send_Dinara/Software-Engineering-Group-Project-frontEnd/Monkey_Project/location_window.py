from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QRadioButton, QPushButton, QLineEdit, QHBoxLayout, QMessageBox, QScrollArea
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import json

class RadioButtonListDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Location Dialog Window")
        self.setFixedSize(400, 500)  # Set fixed size to 400x500

        self.label = QLabel("Choose the location:")
        self.label.setAlignment(Qt.AlignLeft)

        # Scroll area to hold radio button layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # Allow the scroll area to resize its widget
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setObjectName("scroll_area_widget")
        #self.scroll_area_widget.setObjectName("scroll_area")
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setStyleSheet("QScrollArea {background-color:red;}")

        # Button to add a new radio button
        self.add_button = QPushButton("Add Location...")
        self.add_button.setObjectName("add_button")
        self.add_button.setFixedWidth(120)  # Set fixed width to avoid resizing
        self.add_button.clicked.connect(self.add_radiobutton)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.label) 
        main_layout.addWidget(self.scroll_area)

        # Create a QHBoxLayout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)  # Add the "Add Location" button

        # Add spacer to push OK and Cancel buttons to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)

        # OK and Cancel buttons
        self.ok_button = QPushButton("OK")
        self.ok_button.setObjectName("ok_button")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("cancel_button")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)  # Add button layout to main layout

        self.selected_radio_button = None

        self.ok_button.clicked.connect(self.accept)

        # Load radio button state from file
        self.load_radio_button_state()

        # Set the widget to the scroll area
        self.scroll_area.setWidget(self.scroll_area_widget)
    
    def get_selected_radio_buttons(self):
        return self.selected_radio_button
    
    def accept(self):
        # Store selected radio button names when OK button is clicked
        self.selected_radio_button = [radio_button.text() for radio_button in self.findChildren(QRadioButton) if radio_button.isChecked()]
        self.selected_radio_button = ", ".join(self.selected_radio_button)  # Convert list to comma-separated string
        super().accept()
        print(self.selected_radio_button)

    def load_radio_button_state(self):
        try:
            with open("radio_button_state.json", "r") as file:
                state = json.load(file)
                for button_name in state:
                    new_radiobutton = QRadioButton(button_name)
                    self.scroll_area_layout.addWidget(new_radiobutton)

                    # Create delete button with icon
                    delete_button = QPushButton()
                    delete_button.setObjectName("delete_button")
                    delete_button.setText("") 
                    delete_button.setIcon(QIcon("Software-Engineering-Group-Project-frontEnd\Monkey_Project\icon\delete-64.png"))  # Provide the path to your icon
                    delete_button.setIconSize(QSize(16, 16))  # Set the icon size
                    delete_button.setFixedSize(30, 30)  # Set fixed size for the button
                    delete_button.clicked.connect(lambda _, rb=new_radiobutton: self.delete_radiobutton(rb))

                    hbox_layout = QHBoxLayout()
                    hbox_layout.addWidget(new_radiobutton)
                    hbox_layout.addWidget(delete_button)
                    self.scroll_area_layout.addLayout(hbox_layout)
        except FileNotFoundError:
            pass

    def add_radiobutton(self):
     # Create a dialog to input the name of the radio button
        dialog = NameInputDialog()
        result = dialog.exec_()
    
     # If the user pressed Ok, add the radio button
        if result == QDialog.Accepted:
            button_name = dialog.get_name()
            new_radiobutton = QRadioButton(button_name)
            self.scroll_area_layout.addWidget(new_radiobutton)
            delete_button = QPushButton("")
            delete_button.setObjectName("delete_button")
            delete_button.setIcon(QIcon("Software-Engineering-Group-Project-frontEnd\Monkey_Project\icon\delete-64.png"))  # Provide the path to your icon
            delete_button.setIconSize(QSize(16, 16))  # Set the icon size
            delete_button.setFixedSize(30, 30)  # Set fixed size for the button
            delete_button.clicked.connect(lambda _, rb=new_radiobutton: self.delete_radiobutton(rb))
            hbox_layout = QHBoxLayout()
            hbox_layout.addWidget(new_radiobutton)
            hbox_layout.addWidget(delete_button)
            self.scroll_area_layout.addLayout(hbox_layout)
            self.save_radio_button_state()

    
    def delete_radiobutton(self, radiobutton):
        for i in range(self.scroll_area_layout.count()):
            layout_item = self.scroll_area_layout.itemAt(i)
            if isinstance(layout_item, QHBoxLayout):
                if layout_item.indexOf(radiobutton) != -1:
                    # Delete the layout containing the radio button and delete button
                    delete_button = layout_item.itemAt(1).widget()  # Get the delete button
                    delete_button.deleteLater()  # Delete the delete button widget
                    self.scroll_area_layout.removeItem(layout_item)  # Remove the layout from the scroll area layout
                    radiobutton.deleteLater()  # Delete the radio button widget
                    break
        self.save_radio_button_state()


    def save_radio_button_state(self):
        state = []
        for i in range(self.scroll_area_layout.count()):
            layout_item = self.scroll_area_layout.itemAt(i)
            if isinstance(layout_item, QHBoxLayout):
                radio_button = layout_item.itemAt(0).widget()
                state.append(radio_button.text())
        with open("radio_button_state.json", "w") as file:
            json.dump(state, file)

class NameInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Location Name")

        # Layout for the input field and buttons
        layout = QVBoxLayout()

        # Line edit for inputting radio button name
        self.input_lineedit = QLineEdit()
        self.input_lineedit.setPlaceholderText("Enter Location Name")
        layout.addWidget(self.input_lineedit)

        # Ok and Cancel buttons
        okay_button = QPushButton("OK")
        okay_button.setObjectName("okay_button")
        okay_button.clicked.connect(self.accept)
        cancel_button_ = QPushButton("Cancel")
        cancel_button_.setObjectName("cancel_button_")
        cancel_button_.clicked.connect(self.reject)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(okay_button)
        button_layout.addWidget(cancel_button_)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_name(self):
        # Return the text entered in the line edit
        return self.input_lineedit.text()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    
    dialog = RadioButtonListDialog()
    dialog.show()
    sys.exit(app.exec())
