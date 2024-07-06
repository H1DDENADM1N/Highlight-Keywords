from abc import abstractmethod
from pathlib import Path


# 定义策略接口
class HighlightStrategy:
    @abstractmethod
    def __init__(self, KEYWORDS: frozenset[str]):
        pass

    @abstractmethod
    def highlight(self, content: str) -> str:
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        pass


# 具体策略实现
class MarkdownHighlightStrategy(HighlightStrategy):
    def __init__(self, KEYWORDS: frozenset[str]):
        super().__init__(KEYWORDS)
        self._KEYWORDS = KEYWORDS

    def highlight(self, content: str) -> str:
        for keyword in self._KEYWORDS:
            content = content.replace(keyword, rf" `{keyword}` ")
        return content

    def get_file_extension(self) -> str:
        return ".md"


class TextHighlightStrategy(HighlightStrategy):
    def __init__(self, KEYWORDS: frozenset[str]):
        super().__init__(KEYWORDS)
        self._KEYWORDS = KEYWORDS

    def highlight(self, content: str) -> str:
        for keyword in self._KEYWORDS:
            content = content.replace(keyword, rf" ❗{keyword}❗ ")
        return content

    def get_file_extension(self) -> str:
        return ".txt"


class HtmlHighlightStrategy(HighlightStrategy):
    def __init__(self, KEYWORDS: frozenset[str]):
        super().__init__(KEYWORDS)
        self._KEYWORDS = KEYWORDS

    def highlight(self, content: str) -> str:
        for keyword in self._KEYWORDS:
            content = content.replace(
                keyword,
                rf" <span style='background-color:rgba(255, 255, 0, 0.5)'>{keyword}</span> ",
            )
        return content

    def get_file_extension(self) -> str:
        return ".html"


def get_keywords() -> frozenset:
    script_path: Path = Path(__file__).resolve().parent
    keywords_file: Path = script_path / "KEYWORDS.txt"

    if not keywords_file.exists():
        raise FileNotFoundError(f"关键词文件 {keywords_file} 不存在")

    keywords_list: list = []
    with keywords_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                keywords_list.append(line)

    return frozenset(keywords_list)


def single_file_highlight(file_path: Path, strategy: HighlightStrategy):
    output_file_path = file_path.with_name(
        file_path.stem + "_highlighted" + strategy.get_file_extension()
    )
    with output_file_path.open("w", encoding="utf-8") as output_file:
        with file_path.open("r", encoding="utf-8") as input_file:
            output_file.write(strategy.highlight(input_file.read()))
            print(f"文件 {file_path} 已高亮并保存至 {output_file_path}")


def folder_files_highlight(folder_path: Path, strategy: HighlightStrategy):
    for file_path in folder_path.iterdir():
        if file_path.is_file():
            single_file_highlight(file_path, strategy)


def cli():
    selected_path: Path = Path(input("请输入要高亮的文本文件路径："))
    if not selected_path.exists():
        print("文件不存在，请检查路径是否正确。")
        exit()

    selected_strategy = input("请选择高亮策略（1: Markdown, 2: Text, 3: HTML）：")
    match selected_strategy:
        case "1":
            strategy = MarkdownHighlightStrategy(get_keywords())
        case "2":
            strategy = TextHighlightStrategy(get_keywords())
        case "3":
            strategy = HtmlHighlightStrategy(get_keywords())
        case _:
            print("输入的策略编号不正确，请重新输入。")
            exit()

    if selected_path.is_file():
        single_file_highlight(selected_path, strategy)
    elif selected_path.is_dir():
        folder_files_highlight(selected_path, strategy)
    else:
        print("输入路径既不是文件也不是目录，请检查路径是否正确。")
        exit()


def gui():
    pass
