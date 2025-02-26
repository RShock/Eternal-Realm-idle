from PIL import Image


def convert_grayscale_to_alpha(input_path, output_path):
    # 打开原始图片并转换为RGBA模式
    img = Image.open(input_path).convert('RGBA')

    # 创建灰度图用于生成Alpha通道
    gray = img.convert('L')

    # 将灰度转换为Alpha值（灰度越高越透明）
    alpha_data = [(255 - g) for g in gray.getdata()]

    # 创建新图像并应用Alpha通道
    img.putalpha(Image.new('L', img.size))
    img.putdata(list(zip(
        [p[0] for p in img.getdata()],
        [p[1] for p in img.getdata()],
        [p[2] for p in img.getdata()],
        alpha_data
    )))

    # 保存处理后的图片
    img.save(output_path, 'PNG')


# 使用示例
if __name__ == "__main__":
    convert_grayscale_to_alpha('C:\\Users\\41864\\PycharmProjects\\pythonProject2\\未标题-1.png', 'output.png')