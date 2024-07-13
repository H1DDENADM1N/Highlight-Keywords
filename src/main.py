import sys
from pathlib import Path

from loguru import logger
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFileDialog, QWidget

from .cmd_text_edit import CMDTextEdit
from .strategy import (
    KEYWORDS_FILE,
    HighlightStrategy,
    HtmlHighlightStrategy,
    MarkdownHighlightStrategy,
    TextHighlightStrategy,
    get_keywords,
)
from .Ui_highlight_keywords import Ui_Form


class HighlightKeywords(QWidget, Ui_Form):
    """Main window class, inherited from QWidget and Ui_Form, for highlighting keywords"""

    def __init__(self, args: list[str]):
        """Initialization methods, setting UI and window properties"""
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("assets/icon.ico"))
        self.setWindowOpacity(0.9)
        self.cte = CMDTextEdit()
        self.verticalLayout_2.addWidget(self.cte)
        self.selected_paths: list[Path] = []
        self.args = args
        self.get_selected_paths_from_args()
        self.selected_strategy: str = self.comboBox_strategy.currentText()
        self.keywords: frozenset[str] = frozenset()
        self.initUI()

    def initUI(self):
        """Initialize event connections for UI components"""
        self.pushButton_select_file.clicked.connect(self.select_file)
        self.pushButton_select_folder.clicked.connect(self.select_folder)
        self.comboBox_strategy.currentTextChanged.connect(self.change_strategy)
        self.pushButton_edit_keywords.clicked.connect(self.edit_keywords)
        self.pushButton_execute.clicked.connect(self.execute)

    def get_selected_paths_from_args(self):
        """Get the path to the selected file from the command line arguments"""
        if len(self.args) > 1:
            logger.info(f"Command line arguments detected: {self.args[1:]}\n")
            for arg in self.args[1:]:
                path = Path(arg)
                if path.exists() and path.is_file():
                    self.selected_paths.append(path)
                else:
                    logger.warning(
                        f"The command line argument {arg} is not a valid file path and has been ignored. \n"
                    )
            self.update_selected_paths_display()

    def select_file(self):
        """Callback method for select files"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", "All Files (*)"
        )
        self.selected_paths = [Path(file_path) for file_path in file_paths]
        self.update_selected_paths_display()

    def select_folder(self):
        """Callback method for select a folder"""
        folder_path = QFileDialog.getExistingDirectory(self, "Select a Folder", "")
        if folder_path:
            self.selected_paths = [Path(folder_path)]
            self.plainTextEdit_selected_path.setPlainText(
                f"Selected folder: {folder_path}"
            )
        else:
            self.selected_paths = []
            self.plainTextEdit_selected_path.setPlainText("Cancelled Select a Folder")

    def change_strategy(self):
        """Callback methods for change the highlight strategy"""
        self.selected_strategy = self.comboBox_strategy.currentText()
        logger.info(f"Selected Strategy: {self.selected_strategy}\n")

    def edit_keywords(self):
        """Callback methods for editing keywords"""
        self.cte.run_cmd(f"notepad.exe {KEYWORDS_FILE}")

    def execute(self):
        """Callback method to perform highlight"""
        if not self.selected_paths:
            logger.info("Please select files or a folder first.\n")
            return

        logger.info("Start highlighting...\n")

        self.keywords = get_keywords()
        logger.info(f"Keywords: {', '.join(self.keywords)}\n")

        execute_strategy = self.get_highlight_strategy()

        try:
            for selected_path in self.selected_paths:
                if selected_path.is_file():
                    self.single_file_highlight(selected_path, execute_strategy)
                elif selected_path.is_dir():
                    self.folder_files_highlight(selected_path, execute_strategy)
                else:
                    logger.critical(
                        f"The selected path {selected_path} is not a file or a directory, please check if the path is correct.\n"
                    )
        except Exception as e:
            logger.error(f"An error occurred while executing highlight: {e}\n")
        else:
            logger.info("Highlighting is complete...\n")
            self.cte.append_log("\x1b[94m\x1b[92mHighlighting is complete...\x1b[0m")

    def get_highlight_strategy(self):
        """Get the highlight strategy based on the selected strategy from QComboBox"""
        match self.selected_strategy:
            case "1. Markdown":
                return MarkdownHighlightStrategy(self.keywords)
            case "2. Text":
                return TextHighlightStrategy(self.keywords)
            case "3. HTML":
                return HtmlHighlightStrategy(self.keywords)
            case _:
                logger.critical(
                    "Unknown highlighting strategy, use Markdown strategy as default.\n"
                )
                return MarkdownHighlightStrategy(self.keywords)

    def single_file_highlight(
        self, file_path: Path, execute_strategy: HighlightStrategy
    ):
        """Highlighting of individual documents"""
        output_file_path = file_path.with_name(
            file_path.stem + "_highlighted" + execute_strategy.get_file_extension()
        )
        try:
            with file_path.open(
                "r", encoding="utf-8"
            ) as input_file, output_file_path.open(
                "w", encoding="utf-8"
            ) as output_file:
                output_file.write(execute_strategy.highlight(input_file.read()))
                logger.info(
                    f"File {file_path} is highlighted and saved to {output_file_path}\n"
                )
        except UnicodeDecodeError:
            logger.critical(
                f"File {file_path} could not be read in UTF-8, please check the file encoding.\n"
            )
            self.delete_output_file(output_file_path)

    def folder_files_highlight(
        self, folder_path: Path, execute_strategy: HighlightStrategy
    ):
        """Highlight all files in the folder"""
        for file_path in folder_path.iterdir():
            if file_path.is_file() and "_highlighted" not in file_path.name:
                self.single_file_highlight(file_path, execute_strategy)

    def delete_output_file(self, output_file_path: Path):
        """Delete the output file when an error occurs during highlighting"""
        try:
            output_file_path.unlink()
        except Exception as e:
            logger.error(f"Delete output file {output_file_path} Failed: {e}\n")

    def update_selected_paths_display(self):
        """Update the QPlainTextEdit to display the list of selected paths"""
        self.plainTextEdit_selected_path.setPlainText(
            f"Selected files:\n{'\n'.join(str(path) for path in self.selected_paths)}"
        )


def main():
    """Main function to start the application"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HighlightKeywords(sys.argv)
    window.show()
    app.exec()
