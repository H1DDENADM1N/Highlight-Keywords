from abc import ABC, abstractmethod
from pathlib import Path

SCRIPT_PATH: Path = Path(__file__).resolve().parent
KEYWORDS_FILE: Path = SCRIPT_PATH / "KEYWORDS.txt"


def get_keywords() -> frozenset:
    if not KEYWORDS_FILE.exists():
        raise FileNotFoundError(f"关键词文件 {KEYWORDS_FILE} 不存在")

    keywords_list: list = []
    with KEYWORDS_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                keywords_list.append(line)

    # 去重和去除子串
    unique_keywords = set()
    for keyword in sorted(keywords_list, key=len, reverse=True):
        if not any(keyword in k for k in unique_keywords):
            unique_keywords.add(keyword)

    return frozenset(unique_keywords)


# 定义策略接口
class HighlightStrategy(ABC):
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
