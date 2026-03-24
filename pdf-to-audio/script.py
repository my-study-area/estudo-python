# #file reader
# import pyttsx3
# import fitz 
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QIcon

# class Reader(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.layout = QVBoxLayout()

#         self.label = QLabel("No file selected", self)
#         self.label.setStyleSheet("font-size: 16px; color: #e0e5ec; text-align: center;")
#         self.label.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.label)

#         self.layout2 = QHBoxLayout()
#         self.layout.addLayout(self.layout2)

#         self.input1 = QLineEdit()
#         self.input1.setPlaceholderText("Start")
#         self.input1.setStyleSheet("font-size: 16px; background-color: #e0e5ec; border: 1px ; padding: 10px; border-radius: 10px; ")
#         self.layout2.addWidget(self.input1)

#         self.input2 = QLineEdit()
#         self.input2.setPlaceholderText("End")
#         self.input2.setStyleSheet("font-size: 16px; background-color: #e0e5ec; border: 1px ; padding: 10px; border-radius: 10px; ")
#         self.layout2.addWidget(self.input2)

#         self.btn = QPushButton("Select File", self)
#         self.btn.setStyleSheet("font-size: 16px; background-color: #e0e5ec; border: 1px ; padding: 10px; border-radius: 10px; ")
#         self.btn.clicked.connect(self.showDialog)
#         self.layout.addWidget(self.btn)

#         self.setLayout(self.layout)
#         self.setWindowTitle("Reader")
#         self.resize(400, 400)

#     def showDialog(self):
#         options = QFileDialog.Options()
#         file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
#         global page

#         if file_path:
#             self.label.setText(f"Selected File: {file_path}")
#             start = self.input1.text()
#             stop = self.input2.text()

#             doc = fitz.open(f'{file_path}')
#             text = ""
#             if start == "" and stop == "":
#                 for page in doc:
#                     text += page.get_text()  # Extract text from each page

#             elif start == "":
#                 for i in range(0,int(stop)):
#                         page = doc.load_page(i)
#                         text += page.get_text()  # Extract text from each page

#             elif stop == "":
#                 for i in range(int(start)-1,len(doc)):
#                         page = doc.load_page(i)
#                         text += page.get_text()  # Extract text from each page
#             else:
#                 for i in range(int(start)-1,int(stop)):
#                         page = doc.load_page(i)
#                         text += page.get_text()  # Extract text from each page 


#             engine = pyttsx3.init()
#             engine.say(text)
#             engine.runAndWait()
    

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = Reader()
#     ex.setStyleSheet("background-color: #043e7d")
#     ex.setWindowIcon(QIcon("app_icon.png"))
#     ex.show()
#     sys.exit(app.exec_())




from TTS.api import TTS
print("OK")
