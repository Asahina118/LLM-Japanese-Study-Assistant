from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, pyqtSlot
from PyQt6.QtCore import QMetaObject, Q_ARG
from PyQt6.QtGui import QTextCursor
import subprocess

from MyApp import *
from OllamaLLM import *

class Worker(QObject):
    chunk_received = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    test = pyqtSignal()
    ollama_llm = OllamaLLM()

    @pyqtSlot()
    def emit_test_signal(self) -> None:
        self.test.emit()

    @pyqtSlot(str)
    def get_output_from_llm(self, input_text : str) -> None:
        try:
            for chunk in self.ollama_llm.output_chat_stream(input_text):
                self.chunk_received.emit(chunk)
            
            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))


        return
