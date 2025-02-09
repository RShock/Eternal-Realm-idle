import os
import pyperclip

def output_py_files(folder_path='.'):
    """
    遍历指定文件夹及其子文件夹，输出所有 .py 文件的内容。
    结果将复制到剪贴板。跳过名为 'venv' 的文件夹。
    :param folder_path: 目标文件夹路径，默认为当前文件夹。
    """
    # 获取当前文件的路径
    current_file = os.path.basename(__file__)

    # 保存所有结果的字符串
    output = ""

    # 遍历指定目录下的所有文件和文件夹
    for root, dirs, files in os.walk(folder_path):
        # 跳过 'venv' 文件夹
        if 'venv' in dirs:
            dirs.remove('venv')

        for filename in files:
            # 只处理以 .py 结尾且不是当前脚本的文件
            if (filename.endswith('.py') or filename.endswith('.html') or filename.endswith('css'))and filename != current_file:
                file_path = os.path.join(root, filename)
                output += f"**{file_path} :\n"
                with open(file_path, 'r', encoding='utf-8') as file:
                    output += file.read() + "\n"
                output += "\n" + "=" * 40 + "\n"

    # 将结果复制到剪贴板
    pyperclip.copy(output)
    print("结果已复制到剪贴板。")

# 调用方法，默认遍历当前文件夹
output_py_files()
