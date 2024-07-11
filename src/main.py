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
    """主窗口类，继承自QWidget和Ui_Form，用于高亮关键词"""

    def __init__(self, args: list[str]):
        """初始化方法，设置UI和窗口属性"""
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
        """初始化UI组件的事件连接"""
        self.pushButton_select_file.clicked.connect(self.select_file)
        self.pushButton_select_folder.clicked.connect(self.select_folder)
        self.comboBox_strategy.currentTextChanged.connect(self.change_strategy)
        self.pushButton_edit_keywords.clicked.connect(self.edit_keywords)
        self.pushButton_execute.clicked.connect(self.execute)

    def get_selected_paths_from_args(self):
        """从命令行参数中获取选择的文件路径"""
        if len(self.args) > 1:
            logger.info(f"检测到命令行参数：{self.args[1:]}\n")
            for arg in self.args[1:]:
                path = Path(arg)
                if path.exists() and path.is_file():
                    self.selected_paths.append(path)
                else:
                    logger.warning(f"命令行参数 {arg} 不是有效的文件路径，已忽略。\n")
            self.update_selected_paths_display()

    def select_file(self):
        """选择文件的回调方法"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "选择文件", "", "All Files (*)"
        )
        self.selected_paths = [Path(file_path) for file_path in file_paths]
        self.update_selected_paths_display()

    def select_folder(self):
        """选择文件夹的回调方法"""
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
        """改变高亮策略的回调方法"""
        self.selected_strategy = self.comboBox_strategy.currentText()
        logger.info(f"已选择策略：{self.selected_strategy}\n")

    def edit_keywords(self):
        """编辑关键词的回调方法"""
        self.cte.run_cmd(f"notepad.exe {KEYWORDS_FILE}")

    def execute(self):
        """执行高亮处理的回调方法"""
        if not self.selected_paths:
            logger.info("请先选择文件或文件夹。\n")
            return

        logger.info("开始执行高亮处理...\n")

        self.keywords = get_keywords()
        logger.info(f"关键词：{', '.join(self.keywords)}\n")

        execute_strategy = self.get_highlight_strategy()

        try:
            for selected_path in self.selected_paths:
                if selected_path.is_file():
                    self.single_file_highlight(selected_path, execute_strategy)
                elif selected_path.is_dir():
                    self.folder_files_highlight(selected_path, execute_strategy)
                else:
                    logger.critical(
                        "已选择的路径不是文件也不是目录，请检查路径是否正确。\n"
                    )
        except Exception as e:
            logger.error(f"执行高亮处理时发生错误：{e}\n")
        else:
            logger.info("高亮处理执行完毕...\n")
            self.cte.append_log("\x1b[94m\x1b[92m高亮处理执行完毕...\x1b[0m")

    def get_highlight_strategy(self):
        """根据选择的策略获取高亮策略实例"""
        match self.selected_strategy:
            case "1. Markdown":
                return MarkdownHighlightStrategy(self.keywords)
            case "2. Text":
                return TextHighlightStrategy(self.keywords)
            case "3. HTML":
                return HtmlHighlightStrategy(self.keywords)
            case _:
                logger.critical("未知的高亮策略，使用 Markdown 策略。\n")
                return MarkdownHighlightStrategy(self.keywords)

    def single_file_highlight(
        self, file_path: Path, execute_strategy: HighlightStrategy
    ):
        """对单个文件进行高亮处理"""
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
                logger.info(f"文件 {file_path} 已高亮并保存至 {output_file_path}\n")
        except UnicodeDecodeError:
            logger.critical(
                f"文件 {file_path} 未能以 UTF-8 编码读取，请检查文件编码。\n"
            )
            self.delete_output_file(output_file_path)

    def folder_files_highlight(
        self, folder_path: Path, execute_strategy: HighlightStrategy
    ):
        """对文件夹中的所有文件进行高亮处理"""
        for file_path in folder_path.iterdir():
            if file_path.is_file() and "_highlighted" not in file_path.name:
                self.single_file_highlight(file_path, execute_strategy)

    def delete_output_file(self, output_file_path: Path):
        """删除输出文件"""
        try:
            output_file_path.unlink()
        except Exception as e:
            logger.error(f"删除输出文件 {output_file_path} 失败：{e}\n")

    def update_selected_paths_display(self):
        """更新已选择路径的显示"""
        self.plainTextEdit_selected_path.setPlainText(
            f"已选择文件：\n{'\n'.join(str(path) for path in self.selected_paths)}"
        )


def main():
    """主函数，启动应用程序"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HighlightKeywords(sys.argv)
    window.show()
    app.exec()
