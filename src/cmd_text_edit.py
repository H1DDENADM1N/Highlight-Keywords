# Enhanced from https://github.com/271374667/VideoFusion/blob/master/src/components/cmd_text_edit.py


import json
import subprocess
import sys
from functools import wraps
from pathlib import Path
from typing import Union

import loguru
from ansi2html import Ansi2HTMLConverter
from PySide6.QtCore import QMutex, Qt, QThread, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget


# from qfluentwidgets.components import TextEdit
# from src.utils import singleton
def singleton(cls):
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


class CmdRunnerThread(QThread):
    append_signal = Signal(str)

    def __init__(self, command, cwd: Path or str, parent=None):
        super().__init__(parent)
        self.command = command
        self.cwd = cwd
        self.mutex = QMutex()

    def run(self):
        try:
            if isinstance(self.command, list):
                command_processed = self.command
            else:
                command_processed = self.command.split()

            proc = subprocess.Popen(
                command_processed,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.cwd,
                shell=True,
            )
            while True:
                output = proc.stdout.readline()
                if proc.poll() is not None and output == "":
                    break
                if output:
                    self.mutex.lock()
                    self.append_signal.emit(output.strip())
                    self.mutex.unlock()
        except Exception as e:
            self.mutex.lock()
            self.append_signal.emit(f"An error occurred: {e}")
            self.mutex.unlock()


@singleton
class CMDTextEdit(QWidget):
    """
    A QTextEdit Widget with ANSI color code support

    Methods.
        - append_log: Add a message.
        - run_cmd: Run a cmd command.

    Signals.
        - append_signal: Adds a signal to a message.

    Note.
        - The color code conversion depends on the `loguru` and `ansi2html` libraries which you need to pip install first.
        - You can use the `loguru` library's `logger` object directly to output logs, which are automatically colored and displayed in a text box.
        - You can use the `run_cmd` method to run a cmd command.
    """

    append_signal = Signal(str)
    window_hidden_signal = Signal()

    def __init__(self, parent=None):
        super().__init__()
        self.setObjectName("cmd_text_edit")
        self._ansi2html_converter = Ansi2HTMLConverter()

        # self.text_edit = TextEdit()
        self.text_edit = QTextEdit()
        # Set the color of the text box CSS style
        self.text_edit.setStyleSheet("background-color: #2d2d2d;")
        self.text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.append_signal.connect(self._append_log_slot)

        # To facilitate direct binding to loguru
        self._hook_loguru()

    def append_log(self, context: str) -> None:
        """Manually add a one-line message"""
        self.append_signal.emit(self._ansi2html(context))
        # 将窗口滚动到底部
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)

    def run_cmd(self, command: Union[str, list[str]]) -> None:
        """Running a cmd command in multiple threads"""
        self.cmd_thread = CmdRunnerThread(command, ".")
        self.cmd_thread.append_signal.connect(self._append_log_slot)
        self.cmd_thread.start()

    def _hook_loguru(self):
        """Configure the loguru logger to process log messages through a custom sink function and add the processed log messages to a text editor."""
        # In order to prevent forgetting to import the loguru library
        import loguru

        def sink(message):
            ansi_color_text = json.loads(str(message))
            self.append_log(ansi_color_text["text"])

        loguru.logger.add(sink, colorize=True, serialize=True)

    def _append_log_slot(self, context: str) -> None:
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)
        self.text_edit.insertHtml(f"{context}<br>")
        # Remove redundant spaces
        self.text_edit.moveCursor(QTextCursor.MoveOperation.End)

    def _ansi2html(self, ansi_content: str) -> str:
        convert = self._ansi2html_converter.convert(
            ansi_content, full=True, ensure_trailing_newline=True
        )

        return self._remove_html_space(convert)

    def _remove_html_space(self, html: str) -> str:
        return (
            html.replace("white-space: pre-wrap", "white-space: nowrap")
            .replace("word-wrap: break-word", "word-wrap: normal")
            .replace(
                "font-size: normal;", "font-size: medium; font-family: sans-serif;"
            )
        )

    def keyPressEvent(self, event):
        # Press ESC to hide
        if event.key() == Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

    def hideEvent(self, event):
        # Press ESC to hide
        self.window_hidden_signal.emit()
        super().hideEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cte = CMDTextEdit()
    cte.show()
    cte.resize(800, 800)
    # Example of running an external command:
    cte.run_cmd("ping 127.0.0.1")
    loguru.logger.info("Hello World!")
    loguru.logger.error("This is an error message")
    loguru.logger.warning("This is a warning message")
    loguru.logger.debug("This is a debug message")
    loguru.logger.critical("我是一段中文日志信息")

    # A green ANSI color code
    # text = "\x1b[94m\x1b[92m我是一个绿色的字\x1b[0m"
    # cte.append_log(text)

    sys.exit(app.exec())
