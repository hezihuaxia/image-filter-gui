import cv2
import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from filters import apply_grayscale, apply_blur, apply_edge, apply_brightness, apply_contrast

def process_images(input_folder, filter_type, param=None):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = f"outputs_{timestamp}"
    os.makedirs(output_folder, exist_ok=True)

    count = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".png", ".jpeg")):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            if img is None:
                continue

            if filter_type == "gray":
                result = apply_grayscale(img)
                suffix = "_gray"
            elif filter_type == "blur":
                result = apply_blur(img)
                suffix = "_blur"
            elif filter_type == "edge":
                result = apply_edge(img)
                suffix = "_edge"
            elif filter_type == "bright":
                result = apply_brightness(img, param)
                suffix = f"_bright{param}"
            elif filter_type == "contrast":
                result = apply_contrast(img, param)
                suffix = f"_contrast{param}"
            else:
                continue

            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_folder, name + suffix + ext)
            cv2.imwrite(output_path, result)
            count += 1

    return count, output_folder


class ImageProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("图像批处理工具")

        self.input_folder = ""
        self.filter_type = tk.StringVar(value="gray")

        # 选择输入文件夹
        self.folder_label = tk.Label(master, text="未选择文件夹")
        self.folder_label.pack(pady=5)

        self.browse_button = tk.Button(master, text="选择图片文件夹", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        # 滤镜选项
        tk.Label(master, text="选择滤镜：").pack(pady=5)
        self.filter_menu = ttk.Combobox(master, textvariable=self.filter_type)
        self.filter_menu['values'] = ("gray", "blur", "edge", "bright", "contrast")
        self.filter_menu.pack()

        # 参数输入（用于亮度/对比度）
        self.param_label = tk.Label(master, text="参数值（亮度/对比度）:")
        self.param_entry = tk.Entry(master)

        self.filter_menu.bind("<<ComboboxSelected>>", self.toggle_param_entry)

        # 开始处理按钮
        self.process_button = tk.Button(master, text="开始处理", command=self.run_processing)
        self.process_button.pack(pady=10)

    def browse_folder(self):
        self.input_folder = filedialog.askdirectory()
        self.folder_label.config(text=self.input_folder)

    def toggle_param_entry(self, event=None):
        if self.filter_type.get() in ("bright", "contrast"):
            self.param_label.pack()
            self.param_entry.pack()
        else:
            self.param_label.pack_forget()
            self.param_entry.pack_forget()

    def run_processing(self):
        if not self.input_folder:
            messagebox.showerror("错误", "请先选择输入文件夹！")
            return

        filter_type = self.filter_type.get()

        # 处理参数
        param = None
        if filter_type == "bright":
            try:
                param = int(self.param_entry.get())
            except ValueError:
                messagebox.showerror("错误", "请输入整数亮度值")
                return
        elif filter_type == "contrast":
            try:
                param = float(self.param_entry.get())
            except ValueError:
                messagebox.showerror("错误", "请输入浮点数对比度值")
                return

        count, output_folder = process_images(self.input_folder, filter_type, param)
        messagebox.showinfo("完成", f"处理完成！共处理了 {count} 张图像。\n输出文件夹：{output_folder}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = ImageProcessorGUI(root)
    root.mainloop()
