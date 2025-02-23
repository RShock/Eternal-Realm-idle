import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from threading import Thread
from queue import Queue


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片批量处理工具 v1.1")
        self.setup_ui()
        self.queue = Queue()
        self.running = False

    def setup_ui(self):
        # 输入文件夹选择
        ttk.Label(self.root, text="输入文件夹:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.input_path = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.input_path, width=40).grid(row=0, column=1, padx=5)
        ttk.Button(self.root, text="选择...", command=self.select_input).grid(row=0, column=2, padx=5)

        # 输出文件夹选择
        ttk.Label(self.root, text="输出文件夹:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.output_path = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.output_path, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(self.root, text="选择...", command=self.select_output).grid(row=1, column=2, padx=5)

        # 压缩质量设置
        ttk.Label(self.root, text="压缩质量 (1-100):").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.quality = tk.IntVar(value=80)
        ttk.Scale(self.root, from_=1, to=100, variable=self.quality, orient='horizontal').grid(row=2, column=1,
                                                                                               columnspan=2,
                                                                                               sticky='we', padx=5)

        # 进度条
        self.progress = ttk.Progressbar(self.root, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, sticky='we', padx=5, pady=5)

        # 日志区域
        self.log_text = tk.Text(self.root, height=10, width=60)  # 变量名改为log_text
        self.log_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        # 控制按钮
        self.start_btn = ttk.Button(self.root, text="开始处理", command=self.start_processing)
        self.start_btn.grid(row=5, column=2, padx=5, pady=5)

    def select_input(self):
        path = filedialog.askdirectory()
        if path:
            self.input_path.set(path)
            self.output_path.set(os.path.join(path, 'output'))

    def select_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_path.set(path)

    def start_processing(self):
        input_dir = self.input_path.get()
        output_dir = self.output_path.get()
        quality = self.quality.get()

        if not os.path.exists(input_dir):
            messagebox.showerror("错误", "输入目录不存在！")
            return

        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        self.start_btn.config(state='disabled')
        self.progress['value'] = 0
        Thread(target=self.process_images, args=(input_dir, output_dir, quality)).start()

    def process_images(self, input_dir, output_dir, quality):
        valid_ext = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
        files = []
        for root, _, filenames in os.walk(input_dir):
            files.extend([
                (root, f)
                for f in filenames
                if f.lower().endswith(valid_ext)
            ])

        total = len(files)
        processed = 0

        for root_dir, filename in files:
            input_path = os.path.join(root_dir, filename)
            try:
                with Image.open(input_path) as img:
                    # 计算相对路径
                    relative_path = os.path.relpath(root_dir, input_dir)
                    output_root = os.path.join(output_dir, relative_path)
                    os.makedirs(output_root, exist_ok=True)

                    # 构建输出路径
                    output_path = os.path.join(output_root, filename)
                    output_path = os.path.splitext(output_path)[0] + '.jpg'

                    # 调整尺寸
                    resized = img.resize((384, 512), Image.LANCZOS)

                    # 保存图片
                    resized.save(
                        output_path,
                        'JPEG',
                        quality=quality,
                        optimize=True,
                        progressive=True
                    )

                    # 使用队列传递日志消息
                    self.queue.put(f"处理成功: {filename}")

            except Exception as e:
                self.queue.put(f"处理失败: {filename} - {str(e)}")

            # 更新进度
            processed += 1
            self.progress['value'] = (processed / total) * 100
            self.root.update_idletasks()

        self.queue.put("COMPLETE")

    def log(self, message):
        self.log.insert('end', message + '\n')
        self.log.see('end')

    def update(self):
        while not self.queue.empty():
            msg = self.queue.get()
            self.log.insert('end', msg + '\n')
        self.root.after(100, self.update)

    def log_message(self, msg):
        self.log_text.insert('end', msg + '\n')
        self.log_text.see('end')


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
