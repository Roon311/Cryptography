import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QTextEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt
import time
import PGP 


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("File Encryption/Decryption")
        self.setGeometry(100, 100, 600, 600)
        self.file_path=None
        # Create GUI elements
        self.title_label = QLabel("File Encryption/Decryption")
        self.title_label.setFont(QFont('Arial', 24))
        self.subtitle_label = QLabel("Select a text file to encrypt and decrypt")
        self.subtitle_label.setFont(QFont('Arial', 14))
        self.select_button = QPushButton("Select File", clicked=self.select_file)
        self.enc_dec_button = QPushButton("Encrypt & Decrypt", clicked=self.encDec)
        self.text_label = QLabel("Plain Text:")
        self.text_label.setFont(QFont('Arial', 14))
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.ciphertext_label = QLabel("Encrypted Text:")
        self.ciphertext_label.setFont(QFont('Arial', 14))
        self.ciphertext_edit = QTextEdit()
        self.ciphertext_edit.setReadOnly(True)
        self.encryption_time_label = QLabel("Encryption Time:")
        self.encryption_time_label.setFont(QFont('Arial', 14))
        self.encryption_time_edit = QLabel()
        self.plaintext_label = QLabel("Decrypted Text:")
        self.plaintext_label.setFont(QFont('Arial', 14))
        self.plaintext_edit = QTextEdit()
        self.plaintext_edit.setReadOnly(True)
        self.decryption_time_label = QLabel("Decryption Time:")
        self.decryption_time_label.setFont(QFont('Arial', 14))
        self.decryption_time_edit = QLabel()
        self.dec_time_label = QLabel("Decryption Time:")
        self.dec_time_label.setFont(QFont('Arial', 14))
        self.dec_time_edit = QLabel()
        self.show_text_button = QPushButton("Show Text", clicked=self.show_text)
        self.hide_text_button = QPushButton("Hide Text", clicked=self.hide_text)
        self.show_ciphertext_button = QPushButton("Show Ciphertext", clicked=self.show_ciphertext)
        self.hide_ciphertext_button = QPushButton("Hide Ciphertext", clicked=self.hide_ciphertext)
        self.show_plaintext_button = QPushButton("Show Plaintext", clicked=self.show_plaintext)
        self.hide_plaintext_button = QPushButton("Hide Plaintext", clicked=self.hide_plaintext)
        self.save_button = QPushButton("Save Results", clicked=self.save_results)
        self.save_button.setEnabled(False)

        # Set up layout
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.title_label, 0, 0, 1, 3, Qt.AlignCenter)
        grid_layout.addWidget(self.subtitle_label, 1, 0, 1, 3, Qt.AlignCenter)
        grid_layout.addWidget(self.select_button, 2, 2, 1, 1, Qt.AlignCenter)
        grid_layout.addWidget(self.enc_dec_button, 2, 1, 1, 1, Qt.AlignCenter)
        grid_layout.addWidget(self.text_label, 3, 0, 1, 1, Qt.AlignRight)
        grid_layout.addWidget(self.text_edit, 3, 1, 1, 1)
        grid_layout.addWidget(self.show_text_button, 3, 2, 1, 1)
        grid_layout.addWidget(self.ciphertext_label, 4, 0, 1, 1, Qt.AlignRight)
        grid_layout.addWidget(self.ciphertext_edit, 4, 1, 1, 1)
        grid_layout.addWidget(self.show_ciphertext_button, 4, 2, 1, 1)
        grid_layout.addWidget(self.plaintext_label, 5, 0, 1, 1, Qt.AlignRight)
        grid_layout.addWidget(self.plaintext_edit, 5, 1, 1, 1)
        grid_layout.addWidget(self.show_plaintext_button, 5, 2, 1, 1)
        grid_layout.addWidget(self.encryption_time_label, 6, 0, 1, 1, Qt.AlignRight)
        grid_layout.addWidget(self.encryption_time_edit, 6, 1, 1, 1)
        grid_layout.addWidget(self.hide_text_button, 3, 2, 1, 1)
        grid_layout.addWidget(self.hide_ciphertext_button, 4, 2, 1, 1)
        grid_layout.addWidget(self.hide_plaintext_button, 5, 2, 1, 1)
        grid_layout.addWidget(self.dec_time_label, 7, 0, 1, 1, Qt.AlignRight)
        grid_layout.addWidget(self.dec_time_edit, 7, 1, 1, 1)
        grid_layout.addWidget(self.save_button, 8, 1, 1, 1, Qt.AlignCenter)

            # Create a vertical layout to hold the grid layout and add some padding
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(grid_layout)
        vertical_layout.addStretch(1)
        vertical_layout.setContentsMargins(50, 50, 50, 50)

        # Set main layout
        self.setLayout(vertical_layout)

    def select_file(self):
        # Open a file dialog to select a file to encrypt/decrypt
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Text Files (*.txt)", options=options)
        if self.file_path:
            # Load the file contents into the text_edit widget
            with open(self.file_path, 'r') as f:
                self.text_edit.setText(f.read())
            # Enable the save button
            self.save_button.setEnabled(True)
    
    def encDec(self):
        if self.file_path:
            Text,ciphertext,encryption_time,plaintext,decryption_time=PGP.tester(self.file_path)
            self.cipher=ciphertext
            self.encrypt=encryption_time
            self.plaintext=plaintext
            self.dectime=decryption_time
            self.encryption_time_edit.setText(str(round(self.encrypt,5))+' seconds')
            self.ciphertext_edit.setText(str(self.cipher))
            self.plaintext_edit.setText(plaintext)
            self.dec_time_edit.setText(str(round(self.dectime, 5))+' seconds')
        else:
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Critical)
            error_box.setWindowTitle("Error")
            error_box.setText("Select a file first.")
            error_box.setStandardButtons(QMessageBox.Close)
            error_box.exec_()



    def show_text(self):
        # Show the text in the text_edit widget
        self.text_edit.show()
        self.hide_text_button.show()
        self.show_text_button.hide()

    def hide_text(self):
        # Hide the text in the text_edit widget
        self.text_edit.hide()
        self.hide_text_button.hide()
        self.show_text_button.show()

    def show_ciphertext(self):
        # Show the ciphertext in the ciphertext_edit widget
        self.ciphertext_edit.show()
        self.hide_ciphertext_button.show()
        self.show_ciphertext_button.hide()

    def hide_ciphertext(self):
        # Hide the ciphertext in the ciphertext_edit widget
        self.ciphertext_edit.hide()
        self.hide_ciphertext_button.hide()
        self.show_ciphertext_button.show()

    def show_plaintext(self):
        # Show the plaintext in the plaintext_edit widget
        self.plaintext_edit.show()
        self.hide_plaintext_button.show()
        self.show_plaintext_button.hide()

    def hide_plaintext(self):
        # Hide the plaintext in the plaintext_edit widget
        self.plaintext_edit.hide()
        self.hide_plaintext_button.hide()
        self.show_plaintext_button.show()

    def save_results(self):
        # Save the results to a text file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)", options=options)
        if file_name:
            # Add ".txt" extension if not present
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            # Write results to file
            with open(file_name, "w") as file:
                file.write("---------------------------------------------Plain Text:---------------------------------------------\n\n")
                file.write(self.text_edit.toPlainText() + "\n\n")
                file.write("---------------------------------------------Encrypted Text:---------------------------------------------\n\n")
                file.write(self.ciphertext_edit.toPlainText() + "\n\n")
                file.write("---------------------------------------------Decrypted Text:---------------------------------------------\n\n")
                file.write(self.plaintext_edit.toPlainText() + "\n\n")
                file.write("---------------------------------------------Performance:---------------------------------------------\n\n")
                file.write("Encryption Time: " + self.encryption_time_edit.text() + "\n")
                file.write("Decryption Time: " + self.dec_time_edit.text() + "\n")

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec_()
