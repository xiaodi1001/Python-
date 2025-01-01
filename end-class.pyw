import tkinter as tk
from tkinter import ttk
import threading
import time
import os
import subprocess
import sys
import ctypes

# 隐藏 CMD 窗口（仅在 Windows 下生效）
if sys.platform == "win32":
    try:
        ctypes.windll.kernel32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except AttributeError:
        print("无法隐藏命令行窗口。")

def restart_explorer():
    """关闭并重启资源管理器"""
    try:
        os.system("taskkill /f /im explorer.exe")  # 关闭资源管理器
        time.sleep(1)
        subprocess.run("start explorer.exe", shell=True)  # 重启资源管理器
    except Exception as e:
        print(f"重启资源管理器失败：{e}")

def on_now_end():
    """点击“现在下课”"""
    restart_explorer()
    print("资源管理器已重启，程序即将退出。")
    root.quit()

def on_continue():
    """点击“继续拖堂”"""
    print("选择继续拖堂，窗口关闭。")
    root.quit()

def auto_restart():
    """30 秒无操作后自动重启资源管理器并关闭程序"""
    for i in range(30, 0, -1):
        countdown_label_var.set(f" {i} 秒后自动关闭所有进程，请尽快做出选择")
        time.sleep(1)
    print("超时未操作，正在重启资源管理器...")
    on_now_end()

def update_progress_bar():
    """更新进度条"""
    for i in range(31):
        progress_var.set(i)  # 设置当前值
        progress_bar.update_idletasks()
        time.sleep(1)

# 禁用窗口控制按钮
def disable_window_controls():
    if sys.platform == "win32":
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        GWL_STYLE = -16
        WS_SYSMENU = 0x00080000
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style & ~WS_SYSMENU)

# 创建主窗口
root = tk.Tk()
root.title("下课提醒")
root.geometry("450x200")
root.attributes("-topmost", True)  # 窗口置顶

# 禁用最大化、最小化和关闭
root.resizable(False, False)
root.update_idletasks()
disable_window_controls()

# 提示信息
label = tk.Label(root, text="已下课5分钟，是否继续上课？", font=("Arial", 14))
label.pack(pady=10)

# 倒计时标签
countdown_label_var = tk.StringVar(value="还有 30 秒自动关闭所有进程，请尽快做出选择")
countdown_label = tk.Label(root, textvariable=countdown_label_var, font=("Arial", 12))
countdown_label.pack(pady=5)

# 进度条
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate", maximum=30, variable=progress_var)
progress_bar.pack(pady=10)

# 按钮
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

now_end_button = tk.Button(button_frame, text="现在下课", font=("Arial", 12), command=on_now_end)
now_end_button.pack(side="left", padx=20)

continue_button = tk.Button(button_frame, text="继续上课", font=("Arial", 12), command=on_continue)
continue_button.pack(side="right", padx=20)

# 启动自动重启线程
threading.Thread(target=auto_restart, daemon=True).start()

# 启动进度条更新线程
threading.Thread(target=update_progress_bar, daemon=True).start()

# 运行主循环
root.mainloop()