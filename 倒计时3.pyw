import tkinter as tk
from tkinter import messagebox
import pygame
import time

# 初始化 pygame 用于播放音效
pygame.mixer.init()

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("倒计时软件")
        self.root.geometry("400x300")
        
        # 初始化倒计时参数
        self.countdown_time = 10
        self.running = False
        
        # 创建界面组件
        self.label = tk.Label(root, text="即将开始录视频", font=("Arial", 16))
        self.label.pack(pady=20)
        
        self.progress = tk.Canvas(root, width=300, height=30, bg="lightgray")
        self.progress.pack(pady=20)
        
        self.progress_bar = self.progress.create_rectangle(0, 0, 300, 30, fill="green")
        
        # 等待 5 秒后启动倒计时
        self.root.after(5000, self.start_countdown)

    def start_countdown(self):
        """开始倒计时"""
        if self.running:
            return

        self.running = True
        self.label.config(text="离开始录视频还有 10 秒")
        self.countdown()

    def countdown(self):
        """倒计时逻辑"""
        if self.countdown_time > 0:
            # 更新倒计时显示
            self.label.config(text=f"还有 {self.countdown_time} 秒")
            
            # 更新进度条
            progress_width = 300 * (self.countdown_time / 10)  # 10 秒倒计时
            self.progress.coords(self.progress_bar, 0, 0, progress_width, 30)
            
            # 减少时间
            self.countdown_time -= 1
            self.root.after(1000, self.countdown)
        else:
            self.end_countdown()

    def end_countdown(self):
        """倒计时结束处理"""
        # 播放音效
        pygame.mixer.music.load("alarm_sound.mp3")  # 请确保有 alarm_sound.mp3 文件
        pygame.mixer.music.play()
        
        # 显示倒计时结束提示
        messagebox.showinfo("倒计时结束", "倒计时结束，开始录视频！")
        
        # 5 秒后关闭应用
        self.root.after(5000, self.close_application)

    def close_application(self):
        """关闭应用"""
        pygame.mixer.music.load("exit_sound.mp3")  # 播放退出音效
        pygame.mixer.music.play()
        self.root.destroy()  # 关闭主窗口，退出程序


# 运行应用
def main():
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()