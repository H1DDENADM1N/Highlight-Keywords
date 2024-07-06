from pathlib import Path

from loguru import logger
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
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cte = CMDTextEdit()
        self.verticalLayout_2.addWidget(self.cte)
        self.selected_path: Path = None
        self.selected_strategy: str = self.comboBox_strategy.currentText()
        self.keywords: frozenset = frozenset()
        self.initUI()

    def initUI(self):
        self.pushButton_select_file.clicked.connect(self.select_file)
        self.pushButton_select_folder.clicked.connect(self.select_folder)
        self.comboBox_strategy.currentTextChanged.connect(self.change_strategy)
        self.pushButton_edit_keywords.clicked.connect(self.edit_keywords)
        self.pushButton_execute.clicked.connect(self.execute)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", "All Files (*)"
        )
        self.selected_path = Path(file_path)
        self.label_selected_path.setText(f"已选择文件：{str(self.selected_path)}")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "选择文件夹", "", QFileDialog.ShowDirsOnly
        )
        self.selected_path = Path(folder_path)
        self.label_selected_path.setText(f"已选择文件夹：{str(self.selected_path)}")

    def change_strategy(self):
        self.selected_strategy = self.comboBox_strategy.currentText()
        logger.info(f"已选择策略：{self.selected_strategy}\n")

    def edit_keywords(self):
        self.cte.run_cmd(f"notepad.exe {KEYWORDS_FILE}")

    def execute(self):
        logger.info("开始执行高亮处理...\n")

        self.keywords = get_keywords()
        logger.info(f"关键词：{', '.join(self.keywords)}\n")

        match self.selected_strategy:
            case "1. Markdown":
                strategy = MarkdownHighlightStrategy(self.keywords)
            case "2. Text":
                strategy = TextHighlightStrategy(self.keywords)
            case "3. HTML":
                strategy = HtmlHighlightStrategy(self.keywords)
            case _:
                logger.critical("未知的高亮策略")
                raise ValueError("未知的高亮策略")

        try:
            if self.selected_path.is_file():
                logger.info(
                    f"正在对文件 {self.selected_path} 进行高亮处理，策略为 {self.selected_strategy}...\n"
                )
                self.single_file_highlight(self.selected_path, strategy)

            elif self.selected_path.is_dir():
                logger.info(
                    f"正在对文件夹 {self.selected_path} 内的所有文件进行高亮处理，策略为 {self.selected_strategy}...\n"
                )
                self.folder_files_highlight(self.selected_path, strategy)
            else:
                logger.critical(
                    "已选择的路径不是文件也不是目录，请检查路径是否正确。\n"
                )
                raise AttributeError(
                    "已选择的路径不是文件也不是目录，请检查路径是否正确。\n"
                )
        except AttributeError:
            logger.info("请先选择文件或文件夹。\n")

    def single_file_highlight(self, file_path: Path, strategy: HighlightStrategy):
        output_file_path = file_path.with_name(
            file_path.stem + "_highlighted" + strategy.get_file_extension()
        )
        with output_file_path.open("w", encoding="utf-8") as output_file:
            with file_path.open("r", encoding="utf-8") as input_file:
                output_file.write(strategy.highlight(input_file.read()))
                # print(f"文件 {file_path} 已高亮并保存至 {output_file_path}")
                logger.info(f"文件 {file_path} 已高亮并保存至 {output_file_path}\n")

    def folder_files_highlight(self, folder_path: Path, strategy: HighlightStrategy):
        file_path_list = []
        for file_path in folder_path.iterdir():
            if file_path.is_file():
                file_path_list.append(file_path)

        for file_path in file_path_list:
            self.single_file_highlight(file_path, strategy)


def gui():
    app = QApplication([])
    window = HighlightKeywords()
    window.show()
    app.exec()
