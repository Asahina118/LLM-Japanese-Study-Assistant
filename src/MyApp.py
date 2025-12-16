import subprocess

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap, QKeySequence, QShortcut, QColor
from PyQt6.QtCore import Qt, QThread

# functions
import button_functions

# classes
from OllamaLLM import *
from Worker import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_layout()
        self.init_thread()

        
    def init_layout(self):
        self.setWindowTitle("Japanese Study Assistant")
        # self.setWindowIcon(QIcon(".ico"))

        main_layout = QHBoxLayout()

        # left
        left_layout = QVBoxLayout()

        # input field for LLM
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("enter the japanese you want to be analyzed")

        # output field for LLM result
        self.output_field = QTextEdit()
        self.output_field.setPlaceholderText("model will respond here")

        # button for submitting prompt
        button_layout = self.button_setup()


        left_layout.addWidget(self.input_field)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(self.output_field)


        main_layout.addLayout(left_layout)


        # right 
        right_layout = QHBoxLayout()

        # image display
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.resize(800, 600)

        # white_pixmap = QPixmap(800, 600)
        white_pixmap = QPixmap(0,0)
        white_pixmap.fill(QColor("white"))

        self.imageLabel.setPixmap(white_pixmap)

        right_layout.addWidget(self.imageLabel)


        main_layout.addLayout(right_layout)


        # shortcut
        self.captureShortcut = QShortcut(QKeySequence("Alt+S"), self)
        self.captureShortcut.activated.connect(self.captureScreen)

        self.setLayout(main_layout)

    def init_thread(self):
        self.thread = QThread(self)
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.worker.error.connect(self.on_error_received)
        self.worker.chunk_received.connect(self.on_chunk_received)

        

    def captureScreen(self):
        screen = QApplication.primaryScreen()
        if screen:
            # Capture the entire screen (window 0 means full screen)
            pixmap = screen.grabWindow(0)
            # Resize the pixmap to fit imageLabel if needed
            self.imageLabel.resize(800, 600)
            pixmap = pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)

            self.imageLabel.setPixmap(pixmap)
    
    def button_setup(self) -> QHBoxLayout:
        self.button_submit = QPushButton("Analyze")
        self.button_show_thinking = QPushButton("Show thinking")
        self.button_start_ollama_server = QPushButton(
            icon=QIcon("../resources/ollama.ico"),
            text="Start Server"
            )

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.button_submit)
        button_layout.addWidget(self.button_show_thinking)
        button_layout.addWidget(self.button_start_ollama_server)

        return button_layout
    
    # override function. DO NOT change the name
    def closeEvent(self, a0):
        if hasattr(self, "thread"):
            self.thread.quit()
            self.thread.wait(3000)

        command = ["taskkill", "/IM", "ollama.exe", "/F"]
        try:
            subprocess.run(command, shell=True)
        except:
            pass

        return super().closeEvent(a0)
        

    # worker signal
    def on_chunk_received(self, chunk : str):
        self.output_field.insertPlainText(chunk)
        self.output_field.moveCursor(QTextCursor.MoveOperation.End)
        QApplication.processEvents()


    def on_error_received(self, err_msg : str):
        self.output_field.setTextColor(QColor(255, 0, 0))
        self.output_field.append(f"[ERROR] {str(err_msg)}")
        print(str(err_msg))
        self.output_field.setTextColor(QColor(0, 0, 0))