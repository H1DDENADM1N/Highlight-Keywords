from pathlib import Path

from .strategy import (
    HighlightStrategy,
    HtmlHighlightStrategy,
    MarkdownHighlightStrategy,
    TextHighlightStrategy,
    get_keywords,
)


def single_file_highlight(file_path: Path, execute_strategy: HighlightStrategy):
    output_file_path = file_path.with_name(
        file_path.stem + "_highlighted" + execute_strategy.get_file_extension()
    )
    try:
        with output_file_path.open("w", encoding="utf-8") as output_file:
            with file_path.open("r", encoding="utf-8") as input_file:
                output_file.write(execute_strategy.highlight(input_file.read()))
                print(f"文件 {file_path} 已高亮并保存至 {output_file_path}")
    except UnicodeDecodeError:
        print(f"文件 {file_path} 未能已 UTF-8 编码读取，请检查文件编码。")
        # 删除输出文件
        try:
            output_file_path.unlink()
        except Exception as e:
            print(f"删除输出文件 {output_file_path} 失败：{e}")


def folder_files_highlight(folder_path: Path, execute_strategy: HighlightStrategy):
    file_path_list: list[Path] = []
    for file_path in folder_path.iterdir():
        if file_path.is_file() and "_highlighted" not in file_path.name:
            file_path_list.append(file_path)

    for file_path in file_path_list:
        single_file_highlight(file_path, execute_strategy)


def cli():
    selected_path: Path = Path(input("请输入要高亮的文本文件路径："))
    if not selected_path.exists():
        print("文件不存在，请检查路径是否正确。")
        exit()

    selected_strategy = input("请选择高亮策略（1: Markdown, 2: Text, 3: HTML）：")
    match selected_strategy:
        case "1":
            execute_strategy = MarkdownHighlightStrategy(get_keywords())
        case "2":
            execute_strategy = TextHighlightStrategy(get_keywords())
        case "3":
            execute_strategy = HtmlHighlightStrategy(get_keywords())
        case _:
            print("输入的策略编号不正确，请重新输入。")
            exit()

    if selected_path.is_file():
        single_file_highlight(selected_path, execute_strategy)
    elif selected_path.is_dir():
        folder_files_highlight(selected_path, execute_strategy)
    else:
        print("输入路径既不是文件也不是目录，请检查路径是否正确。")
        exit()
