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
    def __init__(self, args: list[str]):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("assets/icon.ico"))
        self.setWindowOpacity(0.9)
        self.cte = CMDTextEdit()
        self.verticalLayout_2.addWidget(self.cte)
        self.selected_paths: list[Path] = (
            self.get_selected_paths_from_args(args) if args else []
        )
        self.selected_strategy: str = self.comboBox_strategy.currentText()
        self.keywords: frozenset[str] = frozenset()
        self.initUI()

    def initUI(self):
        self.pushButton_select_file.clicked.connect(self.select_file)
        self.pushButton_select_folder.clicked.connect(self.select_folder)
        self.comboBox_strategy.currentTextChanged.connect(self.change_strategy)
        self.pushButton_edit_keywords.clicked.connect(self.edit_keywords)
        self.pushButton_execute.clicked.connect(self.execute)

    def get_selected_paths_from_args(self, args: list[str]) -> list[Path]:
        selected_paths: list[Path] = []
        if len(args) > 1:
            logger.info(f"检测到命令行参数：{args}\n")
            for arg in args[1:]:
                path = Path(arg)
                if path.exists() and path.is_file():
                    selected_paths.append(path)
                else:
                    logger.warning(f"命令行参数 {arg} 不是有效的文件路径，已忽略。\n")
            self.plainTextEdit_selected_path.setPlainText(
                f"已选择文件：\n{'\n'.join(args[1:])}"
            )
        return selected_paths

    def select_file(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择文件", "", "All Files (*)"
        )
        if file_paths:
            self.selected_paths = [Path(file_path) for file_path in file_paths]
            self.plainTextEdit_selected_path.setPlainText(
                f"已选择文件：\n{'\n'.join(file_paths)}"
            )
        else:
            self.selected_paths = []
            self.plainTextEdit_selected_path.setPlainText("已取消选择文件")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        if folder_path:
            self.selected_paths = [Path(folder_path)]
            self.plainTextEdit_selected_path.setPlainText(
                f"已选择文件夹：{folder_path}"
            )
        else:
            self.selected_paths = []
            self.plainTextEdit_selected_path.setPlainText("已取消选择文件夹")

    def change_strategy(self):
        self.selected_strategy = self.comboBox_strategy.currentText()
        logger.info(f"已选择策略：{self.selected_strategy}\n")

    def edit_keywords(self):
        self.cte.run_cmd(f"notepad.exe {KEYWORDS_FILE}")

    def execute(self):
        if not self.selected_paths:
            logger.info("请先选择文件或文件夹。\n")
            return

        logger.info("开始执行高亮处理...\n")

        self.keywords = get_keywords()
        logger.info(f"关键词：{', '.join(self.keywords)}\n")

        match self.selected_strategy:
            case "1. Markdown":
                execute_strategy = MarkdownHighlightStrategy(self.keywords)
            case "2. Text":
                execute_strategy = TextHighlightStrategy(self.keywords)
            case "3. HTML":
                execute_strategy = HtmlHighlightStrategy(self.keywords)
            case _:
                # This should never happen
                logger.critical("未知的高亮策略，使用 Markdown 策略。\n")
                execute_strategy = MarkdownHighlightStrategy(self.keywords)

        try:
            for selected_path in self.selected_paths:
                if selected_path.is_file():
                    logger.info(
                        f"正在对文件 {selected_path} 进行高亮处理，策略为 {self.selected_strategy}...\n"
                    )
                    self.single_file_highlight(selected_path, execute_strategy)

                elif selected_path.is_dir():
                    logger.info(
                        f"正在对文件夹 {selected_path} 内的所有文件进行高亮处理，策略为 {self.selected_strategy}...\n"
                    )
                    self.folder_files_highlight(selected_path, execute_strategy)
                else:
                    logger.critical(
                        "已选择的路径不是文件也不是目录，请检查路径是否正确。\n"
                    )
        except AttributeError:
            logger.info("请先选择文件或文件夹。\n")
        else:
            logger.info("高亮处理执行完毕...\n")
            self.cte.append_log("\x1b[94m\x1b[92m高亮处理执行完毕...\x1b[0m")

    def single_file_highlight(
        self, file_path: Path, execute_strategy: HighlightStrategy
    ):
        output_file_path = file_path.with_name(
            file_path.stem + "_highlighted" + execute_strategy.get_file_extension()
        )
        try:
            with output_file_path.open("w", encoding="utf-8") as output_file:
                with file_path.open("r", encoding="utf-8") as input_file:
                    output_file.write(execute_strategy.highlight(input_file.read()))
                    # print(f"文件 {file_path} 已高亮并保存至 {output_file_path}")
                    logger.info(f"文件 {file_path} 已高亮并保存至 {output_file_path}\n")
        except UnicodeDecodeError:
            logger.critical(
                f"文件 {file_path} 未能已 UTF-8 编码读取，请检查文件编码。\n"
            )
            # 删除输出文件
            try:
                output_file_path.unlink()
            except Exception as e:
                logger.error(f"删除输出文件 {output_file_path} 失败：{e}\n")

    def folder_files_highlight(
        self, folder_path: Path, execute_strategy: HighlightStrategy
    ):
        file_path_list: list[Path] = []
        for file_path in folder_path.iterdir():
            if file_path.is_file() and "_highlighted" not in file_path.name:
                file_path_list.append(file_path)

        for file_path in file_path_list:
            self.single_file_highlight(file_path, execute_strategy)


def main(args: list[str]):
    app = QApplication(args)
    app.setStyle("Fusion")
    window = HighlightKeywords(args)
    window.show()
    app.exec()
