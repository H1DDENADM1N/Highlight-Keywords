from abc import ABC, abstractmethod
from pathlib import Path

SCRIPT_PATH: Path = Path(__file__).resolve().parent
KEYWORDS_FILE: Path = SCRIPT_PATH / "KEYWORDS.txt"


def get_keywords() -> frozenset[str]:
    if not KEYWORDS_FILE.exists():
        raise FileNotFoundError(f"The keywords file {KEYWORDS_FILE} does not exist.")
    try:
        with KEYWORDS_FILE.open("r", encoding="utf-8") as f:
            keywords_list = [line.strip("\n") for line in f if line.strip("\n")]
    except UnicodeDecodeError:
        keywords_list = [
            f"The keyword file {KEYWORDS_FILE} could not be read in UTF-8 encoding, please check the file encoding."
        ]

    unique_keywords: set[str] = set()
    for keyword in sorted(keywords_list, key=len, reverse=True):
        if not any(keyword in k for k in unique_keywords):
            unique_keywords.add(keyword)

    return frozenset(unique_keywords)


# Defining the Strategy Interface
class HighlightStrategy(ABC):
    def __init__(self, KEYWORDS: frozenset[str]):
        self._KEYWORDS = KEYWORDS

    @abstractmethod
    def highlight(self, content: str) -> str:
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        pass


# Specific strategy implementation
class MarkdownHighlightStrategy(HighlightStrategy):
    def __init__(self, KEYWORDS: frozenset[str]):
        super().__init__(KEYWORDS)

    def highlight(self, content: str) -> str:
        for keyword in self._KEYWORDS:
            content = content.replace(keyword, rf" `{keyword}` ")
        return content

    def get_file_extension(self) -> str:
        return ".md"


class TextHighlightStrategy(HighlightStrategy):
    def __init__(self, KEYWORDS: frozenset[str]):
        super().__init__(KEYWORDS)

    def highlight(self, content: str) -> str:
        for keyword in self._KEYWORDS:
            content = content.replace(keyword, rf" ❗{keyword}❗ ")
        return content

    def get_file_extension(self) -> str:
        return ".txt"


class HtmlHighlightStrategy(HighlightStrategy):
    def __init__(self, KEYWORDS: frozenset[str]):
        super().__init__(KEYWORDS)

    def highlight(self, content: str) -> str:
        for keyword in self._KEYWORDS:
            content = content.replace(
                keyword,
                rf" <span style='background-color:rgba(255, 255, 0, 0.5)'>{keyword}</span> ",
            )
        return content

    def get_file_extension(self) -> str:
        return ".html"
