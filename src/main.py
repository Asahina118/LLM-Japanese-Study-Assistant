import sys
from PyQt6.QtWidgets import QApplication

# functions
import button_functions

# classes
from OllamaLLM import *
from MyApp import *


qt_app = QApplication(sys.argv)
qt_app.setStyleSheet('''
    QWidget {
    font-size: 15px;
    }

    QPushButton {
    font-size: 15px;
    }
''')

app = MyApp()
ollama_llm = OllamaLLM()

button_functions.bind_button_functions(app, app.worker.ollama_llm)

app.resize(1000, 400)
app.show()

sys.exit(qt_app.exec())
