import requests
import random
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/89.0"
]

def save_vulnerability(url, reason):
    """保存检测结果到 vuln.txt 文件"""
    with open("vuln.txt", "a") as file:
        file.write(f"{url} - {reason}\n")

def format_url(url):
    """将输入的 IP 或 URL 格式化为标准的 http://IP 格式"""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return f"http://{url}"  # 默认补全为 http://

def check_unauthorized_access(url):
    """检测是否存在未授权访问"""
    headers = {'User-Agent': random.choice(user_agents)}
    try:
        # 格式化 URL
        url = format_url(url)
        response = requests.get(url, headers=headers, timeout=10)
        # 检查是否能直接访问 Jenkins 后台
        if response.status_code == 200 and ("Dashboard" in response.text or "Jenkins" in response.text):
            save_vulnerability(url, "未授权访问")
            return f"[+] {url} 存在未授权访问\n"
        else:
            return f"[-] {url} 不存在未授权访问\n"
    except requests.RequestException as e:
        return f"[!] 无法访问 {url}: {str(e)}\n"

def run_checks():
    """批量检测入口"""
    urls = []
    try:
        with open(file_path.get(), "r") as file:
            urls = [line.strip() for line in file if line.strip()]
    except Exception as e:
        messagebox.showerror("错误", f"无法读取文件: {str(e)}")
        return

    output_text.delete(1.0, tk.END)  # 清空文本框

    # 启用多线程处理
    def perform_checks():
        for url in urls:
            result = check_unauthorized_access(url)
            output_text.insert(tk.END, result)
            output_text.see(tk.END)

    # 创建并启动新线程
    threading.Thread(target=perform_checks).start()

def select_file():
    """选择目标 URL 文件"""
    file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file:
        file_path.set(file)

root = tk.Tk()
root.title("Jenkins未授权检测工具 by kai_kk")
file_path = tk.StringVar()
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
select_button = tk.Button(button_frame, text="选择 urls.txt", command=select_file)
select_button.pack(side=tk.LEFT, padx=5)
run_button = tk.Button(button_frame, text="run", command=run_checks)
run_button.pack(side=tk.LEFT, padx=5)
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
output_text.pack(pady=10)
root.mainloop()
