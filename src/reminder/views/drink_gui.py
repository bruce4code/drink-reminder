#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视图层 - 喝水提醒界面
负责所有界面相关的操作：显示窗口、处理用户交互
"""

import tkinter as tk
from tkinter import ttk
import random
import threading
import time
import platform
from datetime import datetime
from ..config import SNOOZE_MINUTES


class DrinkGUI:
    """喝水提醒界面类"""

    def __init__(self, controller):
        """
        初始化界面

        Args:
            controller: 控制器对象
        """
        self.controller = controller
        self.root = None
        self.snooze_minutes = SNOOZE_MINUTES

    def show_reminder(self):
        """显示提醒窗口"""
        # 记录提醒次数
        self.controller.record_reminder()

        # 创建窗口
        self.root = tk.Tk()
        self.root.title("💧 喝水提醒")

        # 窗口大小和位置
        window_width = 450
        window_height = 380
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # 设置最小窗口大小
        self.root.minsize(450, 380)

        # 窗口置顶
        self.root.attributes('-topmost', True)

        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')

        # 主框架
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = tk.Label(
            main_frame,
            text="💧 喝水提醒",
            font=("微软雅黑", 18, "bold"),
            fg="#2196F3"
        )
        title_label.pack(pady=(0, 8))

        # 鼓励语
        encouragement = self.controller.get_encouragement()
        msg_label = tk.Label(
            main_frame,
            text=encouragement,
            font=("微软雅黑", 13),
            fg="#333333"
        )
        msg_label.pack(pady=8)

        # 当前时间
        current_time = datetime.now().strftime("%H:%M:%S")
        time_label = tk.Label(
            main_frame,
            text=f"当前时间：{current_time}",
            font=("微软雅黑", 10),
            fg="#666666"
        )
        time_label.pack(pady=4)

        # 统计信息
        stats = self.controller.get_today_stats()
        stats_text = f"今日已喝：{stats['count']} / {stats['goal']} 杯"
        stats_label = tk.Label(
            main_frame,
            text=stats_text,
            font=("微软雅黑", 11, "bold"),
            fg="#4CAF50"
        )
        stats_label.pack(pady=8)

        # 进度条
        progress = stats['progress']
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=8, padx=20)

        progress_bar = ttk.Progressbar(
            progress_frame,
            length=350,
            mode='determinate',
            value=progress
        )
        progress_bar.pack()

        progress_label = tk.Label(
            progress_frame,
            text=f"进度：{progress:.1f}%",
            font=("微软雅黑", 9),
            fg="#666666"
        )
        progress_label.pack(pady=4)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)

        # 已喝水按钮
        drink_btn = tk.Button(
            button_frame,
            text="✓ 已喝水",
            font=("微软雅黑", 10, "bold"),
            bg="#4CAF50",
            fg="white",
            width=10,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.on_drink
        )
        drink_btn.pack(side=tk.LEFT, padx=4)

        # 稍后提醒按钮
        snooze_btn = tk.Button(
            button_frame,
            text="稍后提醒",
            font=("微软雅黑", 10),
            bg="#FF9800",
            fg="white",
            width=10,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.on_snooze
        )
        snooze_btn.pack(side=tk.LEFT, padx=4)

        # 关闭按钮
        close_btn = tk.Button(
            button_frame,
            text="关闭",
            font=("微软雅黑", 10),
            bg="#9E9E9E",
            fg="white",
            width=10,
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.on_close
        )
        close_btn.pack(side=tk.LEFT, padx=4)

        # 播放提示音（跨平台）
        self._play_sound()

        self.root.mainloop()

    def _play_sound(self):
        """播放提示音（跨平台）"""
        system = platform.system()

        try:
            if system == "Windows":
                import winsound
                winsound.Beep(800, 300)
            elif system == "Darwin":  # macOS
                import os
                os.system('afplay /System/Library/Sounds/Glass.aiff')
            elif system == "Linux":
                import os
                os.system('paplay /usr/share/sounds/freedesktop/stereo/bell.oga 2>/dev/null || beep 2>/dev/null')
        except Exception:
            # 如果播放失败，静默跳过
            pass

    def on_drink(self):
        """点击已喝水"""
        current_time, count = self.controller.record_drink()

        # 显示鼓励消息
        messages = [
            f"太棒了！这是今天第 {count} 杯水！💧",
            f"做得好！已经喝了 {count} 杯水了！👍",
            f"继续保持！第 {count} 杯完成！✨"
        ]
        message = random.choice(messages)

        # 创建提示窗口
        tip_window = tk.Toplevel(self.root)
        tip_window.title("提示")
        tip_window.geometry("300x150")
        tip_window.attributes('-topmost', True)

        # 居中
        tip_window.update_idletasks()
        x = (tip_window.winfo_screenwidth() - 300) // 2
        y = (tip_window.winfo_screenheight() - 150) // 2
        tip_window.geometry(f"+{x}+{y}")

        tk.Label(
            tip_window,
            text=message,
            font=("微软雅黑", 12),
            fg="#4CAF50",
            wraplength=250
        ).pack(expand=True)

        tk.Button(
            tip_window,
            text="确定",
            font=("微软雅黑", 10),
            bg="#4CAF50",
            fg="white",
            width=10,
            command=lambda: [tip_window.destroy(), self.root.destroy()]
        ).pack(pady=10)

    def on_snooze(self):
        """稍后提醒"""
        self.root.destroy()
        print(f"稍后提醒：{self.snooze_minutes} 分钟后再次提醒")

        # 启动延迟提醒
        def delayed_reminder():
            time.sleep(self.snooze_minutes * 60)
            self.show_reminder()

        thread = threading.Thread(target=delayed_reminder, daemon=True)
        thread.start()

    def on_close(self):
        """关闭窗口"""
        self.root.destroy()
