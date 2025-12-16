from MyApp import *
from OllamaLLM import *

from PyQt6.QtGui import QTextCursor

import time

# button binding
def bind_button_functions(app : MyApp, ollama_llm : OllamaLLM) -> None:
    app.button_submit.clicked.connect(lambda: get_output_from_llm(app, ollama_llm))

    app.button_show_thinking.clicked.connect(lambda: show_llm_thinking(app, ollama_llm))

    app.button_start_ollama_server.clicked.connect(lambda: init_ollama_server(app.output_field, ollama_llm))


#  NOTE : chunk = {
#     "model" : str
#     "created_at" : str
#     "response" : str
#     "done" : bool
#   }
def get_output_from_llm(app : MyApp, ollama_llm : OllamaLLM) -> None:
    if (not ollama_llm.is_ollama_server_running()):
        msg = "[ERROR] ollama is not running. Please first start the ollama server first"
        print(msg)
        app.output_field.setTextColor(QColor(255, 0, 0))
        app.output_field.insertPlainText(msg)
        app.output_field.setTextColor(QColor(0, 0, 0))

    app.output_field.clear()
    input_text = app.input_field.text() # returns str

    app.thread.start()
    QMetaObject.invokeMethod(
        app.worker,
        "get_output_from_llm",
        Qt.ConnectionType.QueuedConnection,
        Q_ARG(str, input_text),
    ) 


# not yet implemented after switching to ollama
def show_llm_thinking(app : MyApp, ollama_llm : OllamaLLM) -> None:
    ollama_llm.show_thinking = not ollama_llm.show_thinking
    if ollama_llm.show_thinking: 
        app.button_show_thinking.setText("Hide thinking")
    else:
        app.button_show_thinking.setText("Show thinking")


# add to second thread later =.=
def init_ollama_server(output_field : QTextEdit, ollama_llm : OllamaLLM) -> None:
    if (ollama_llm.is_ollama_server_running()):
        msg = "[INFO] ollama server is already running"
        print(msg)
        output_field.setTextColor(QColor(255, 0, 0))
        output_field.setPlainText(msg)
        output_field.setTextColor(QColor(0, 0, 0))
        return

    command = ["ollama", "serve"]

    try:
        ollama_llm.subprocess = subprocess.Popen(
            command,
            text=True,
        )
        time.sleep(1)

        msg = "[SUCCESS] ollama server is running now. You can start analyzing by pressing the 'analyze' button"
        print(msg)
        output_field.setPlainText(msg)

    except PermissionError:
        msg = "[ERROR] ollama server initialization failed due to permission error. Please try running the app in administrator mode."
        print(msg)
        output_field.setTextColor(QColor(255, 0, 0))
        output_field.setPlainText(msg)
        output_field.setTextColor(QColor(0, 0, 0))