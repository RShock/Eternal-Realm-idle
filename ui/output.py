import os
import pyperclip


def output_files(folder_path='.', show_stats=True):
    """
    遍历指定文件夹及其子文件夹，输出所有文件的内容，并统计行数和字符数。
    跳过 'package.json'、'package-lock.json' 文件和 'node_modules' 文件夹。
    结果将复制到剪贴板。
    :param folder_path: 目标文件夹路径，默认为 'src' 文件夹。
    :param show_stats: 是否显示每个文件的行数和字符数，默认为 True。
    """
    # 获取当前文件的路径
    current_file = os.path.basename(__file__)

    # 保存所有结果的字符串
    output = ""

    # 遍历指定目录下的所有文件和文件夹
    for root, dirs, files in os.walk(folder_path):
        # 跳过 'node_modules' 文件夹
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if 'dist' in dirs:
            dirs.remove('dist')

        for filename in files:
            # 跳过 'package.json' 和 'package-lock.json' 文件
            if filename in ['package.json', 'package-lock.json', 'output.py']:
                continue

            # 处理所有文件类型
            file_path = os.path.join(root, filename)
            output += f"**{file_path} :\n"

            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                output += file_content + "\n"

                # 统计文件的行数和字符数
                lines = file_content.splitlines()
            output += "\n" + "=" * 40 + "\n"

    # 将结果复制到剪贴板
    pyperclip.copy(output)
    print("结果已复制到剪贴板。")

    # 打印行数和字符数的统计信息（仅在 show_stats 为 True 时）
    if show_stats:
        total_files = len(output.split('='))
        total_lines = sum([len(file_content.splitlines()) for file_content in output.split('=') if file_content.strip()])
        total_chars = sum([len(file_content) for file_content in output.split('=') if file_content.strip()])

        print("统计信息：")
        print(f"总文件数: {total_files - 1}")
        print(f"总行数: {total_lines}")
        print(f"总字符数: {total_chars}")


# 调用方法，默认遍历 'src' 文件夹
output_files()
