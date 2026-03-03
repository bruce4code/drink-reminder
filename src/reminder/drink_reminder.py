#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
喝水提醒程序
功能：9:30-18:30每30分钟提醒喝水，统计每日喝水次数
"""

import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime, time as dt_time
import time
import threading

class DrinkReminder:
    def __init__(self):
        self.data_file = "drink_log.json"
        self.start_time = (9, 30)  # 开始提醒时间（小时, 分钟）
        self.end_time = (18, 30)   # 结束提醒时间（小时, 分钟）
        self.interval_minutes = 30  # 提醒间隔（分钟）
        self.daily_goal = 8  # 每日目标喝水次数
        
        # 确保数据文件在项目根目录
        if not os.path.isabs(self.data_file):
            # 获取项目根目录（main.py所在目录）
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.data_file = os.path.join(root_dir, self.data_file)
        
        self.load_data()
        
    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except:
                self.data = self.create_empty_data()
        else:
            self.data = self.create_empty_data()
        
        # 检查日期，如果是新的一天，重置数据
        today = datetime.now().strftime("%Y-%m-%d")
        if self.data.get("current_date") != today:
            self.reset_today(today)
    
    def create_empty_data(self):
        """创建空数据结构"""
        today = datetime.now().strftime("%Y-%m-%d")
        return {
            "current_date": today,
            "today": {
                "count": 0,
                "reminded": 0,
                "times": []
            },
            "history": {}
        }
    
    def reset_today(self, today):
        """重置今日数据"""
        # 保存昨天的数据到历史
        if self.data.get("current_date"):
            old_date = self.data["current_date"]
            self.data["history"][old_date] = self.data["today"].copy()
        
        # 重置今日数据
        self.data["current_date"] = today
        self.data["today"] = {
            "count": 0,
            "reminded": 0,
            "times": []
        }
        
        # 只保留最近7天的历史
        if len(self.data["history"]) > 7:
            dates = sorted(self.data["history"].keys())
            for old_date in dates[:-7]:
                del self.data["history"][old_date]
        
        self.save_data()
    
    def save_data(self):
        """保存数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败: {e}")
    
    def record_drink(self):
        """记录喝水"""
        current_time = datetime.now().strftime("%H:%M")
        self.data["today"]["count"] += 1
        self.data["today"]["times"].append(current_time)
        self.save_data()
        print(f"[{current_time}] 记录喝水，今日第 {self.data['today']['count']} 次")
    
    def record_reminder(self):
        """记录提醒次数"""
        self.data["today"]["reminded"] += 1
        self.save_data()
    
    def get_progress(self):
        """获取进度"""
        count = self.data["today"]["count"]
        return min(count / self.daily_goal * 100, 100)
    
    def get_encouragement(self):
        """获取鼓励语"""
        count = self.data["today"]["count"]
        reminded = self.data["today"]["reminded"]
        
        if reminded == 0:
            return "该喝水啦！"
        
        rate = count / reminded if reminded > 0 else 0
        
        if rate >= 0.8:
            messages = [
                "太棒了！继续保持！💪",
                "做得很好！你是喝水小能手！🌟",
                "完美！健康生活从喝水开始！✨"
            ]
        elif rate >= 0.5:
            messages = [
                "不错哦！再接再厉！👍",
                "保持下去，你能做到的！💧",
                "很好！继续努力！🎯"
            ]
        else:
            messages = [
                "喝水太少啦！要多喝水哦~😊",
                "别忘了喝水！身体需要水分！💦",
                "来喝水吧！为了健康！🌈"
            ]
        
        import random
        return random.choice(messages)

class DrinkReminderGUI:
    def __init__(self, reminder):
        self.reminder = reminder
        self.root = None
        self.snooze_minutes = 10  # 稍后提醒的分钟数
        
    def show_reminder(self):
        """显示提醒窗口"""
        self.reminder.record_reminder()
        
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
        encouragement = self.reminder.get_encouragement()
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
        count = self.reminder.data["today"]["count"]
        reminded = self.reminder.data["today"]["reminded"]
        stats_text = f"今日已喝：{count} / {self.reminder.daily_goal} 杯"
        stats_label = tk.Label(
            main_frame,
            text=stats_text,
            font=("微软雅黑", 11, "bold"),
            fg="#4CAF50"
        )
        stats_label.pack(pady=8)
        
        # 进度条
        progress = self.reminder.get_progress()
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
        import platform
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
        except Exception as e:
            # 如果播放失败，静默跳过
            pass
        
        self.root.mainloop()
    
    def on_drink(self):
        """点击已喝水"""
        self.reminder.record_drink()
        
        # 显示鼓励消息
        count = self.reminder.data["today"]["count"]
        messages = [
            f"太棒了！这是今天第 {count} 杯水！💧",
            f"做得好！已经喝了 {count} 杯水了！👍",
            f"继续保持！第 {count} 杯完成！✨"
        ]
        import random
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

def main():
    """主函数"""
    print("="*50)
    print("  💧 喝水提醒程序启动")
    print(f"  开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  提醒规则: 9:30-18:30每30分钟提醒一次")
    print("="*50)
    print()
    
    reminder = DrinkReminder()
    
    # 显示今日统计
    count = reminder.data["today"]["count"]
    reminded = reminder.data["today"]["reminded"]
    print(f"今日已喝水：{count} 次")
    print(f"今日已提醒：{reminded} 次")
    print()
    
    while True:
        try:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute
            
            # 创建当前时间对象用于比较
            current_time = current_hour * 60 + current_minute  # 转换为分钟数
            start_time_minutes = reminder.start_time[0] * 60 + reminder.start_time[1]
            end_time_minutes = reminder.end_time[0] * 60 + reminder.end_time[1]
            
            # 检查是否在提醒时间范围内（9:30-18:30）
            if start_time_minutes <= current_time <= end_time_minutes:
                # 检查是否是整点或半点
                if current_minute == 0 or current_minute == 30:
                    print(f"[{now.strftime('%H:%M:%S')}] 触发提醒")
                    
                    # 显示提醒窗口
                    gui = DrinkReminderGUI(reminder)
                    gui.show_reminder()
                    
                    # 等待到下一分钟，避免重复提醒
                    time.sleep(60)
            
            # 每10秒检查一次
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n\n程序已停止")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
