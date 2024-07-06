from pathlib import Path

from .strategy import (
    get_keywords,
    HighlightStrategy,
    HtmlHighlightStrategy,
    MarkdownHighlightStrategy,
    TextHighlightStrategy,
)


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
