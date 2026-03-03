#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制器层 - 喝水提醒控制器
负责协调模型和视图，处理时间检测和业务逻辑
"""

import time
from datetime import datetime
from ..models import DrinkData
from ..views import DrinkGUI
from ..config import (
    REMINDER_START_TIME,
    REMINDER_END_TIME,
    REMINDER_INTERVAL
)


def parse_time_str(time_str):
    """解析时间字符串为(小时, 分钟)元组
    
    Args:
        time_str: 时间字符串，格式为 "HH:MM"
        
    Returns:
        tuple: (小时, 分钟)
    """
    hours, minutes = map(int, time_str.split(':'))
    return hours, minutes


class ReminderController:
    """喝水提醒控制器"""

    def __init__(self):
        """初始化控制器"""
        self.model = DrinkData()
        self.start_time = parse_time_str(REMINDER_START_TIME)
        self.end_time = parse_time_str(REMINDER_END_TIME)
        self.interval_seconds = REMINDER_INTERVAL
        self.last_reminder_time = None

    def record_drink(self):
        """记录喝水

        Returns:
            tuple: (当前时间, 今日喝水次数)
        """
        current_time, count = self.model.record_drink()
        print(f"[{current_time}] 记录喝水，今日第 {count} 次")
        return current_time, count

    def record_reminder(self):
        """记录提醒次数"""
        self.model.record_reminder()

    def get_progress(self):
        """获取进度百分比

        Returns:
            float: 进度百分比（0-100）
        """
        return self.model.get_progress()

    def get_encouragement(self):
        """获取鼓励语

        Returns:
            str: 鼓励语
        """
        return self.model.get_encouragement()

    def get_today_stats(self):
        """获取今日统计信息

        Returns:
            dict: 今日统计信息
        """
        return self.model.get_today_stats()

    def get_history(self):
        """获取历史记录

        Returns:
            dict: 历史记录
        """
        return self.model.get_history()

    def is_reminder_time(self, current_hour, current_minute):
        """判断是否是提醒时间

        Args:
            current_hour: 当前小时
            current_minute: 当前分钟

        Returns:
            bool: 是否应该提醒
        """
        # 转换为分钟数便于比较
        current_time = current_hour * 60 + current_minute
        start_time_minutes = self.start_time[0] * 60 + self.start_time[1]
        end_time_minutes = self.end_time[0] * 60 + self.end_time[1]

        # 检查是否在时间范围内
        if start_time_minutes <= current_time <= end_time_minutes:
            # 检查是否是间隔时间点
            minutes_since_start = current_time - start_time_minutes
            interval_minutes = self.interval_seconds // 60
            if minutes_since_start % interval_minutes == 0:
                # 检查距离上次提醒是否已经过了足够的时间
                now = datetime.now()
                current_key = (now.hour, now.minute)
                if self.last_reminder_time != current_key:
                    self.last_reminder_time = current_key
                    return True
        return False

    def show_reminder(self):
        """显示提醒窗口"""
        gui = DrinkGUI(self)
        gui.show_reminder()

    def run(self):
        """运行主循环"""
        print("="*50)
        print("  💧 喝水提醒程序启动")
        print(f"  开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  提醒规则: {self.start_time[0]:02d}:{self.start_time[1]:02d}-"
              f"{self.end_time[0]:02d}:{self.end_time[1]:02d} 每{self.interval_seconds // 60}分钟提醒一次")
        print("="*50)
        print()

        # 显示今日统计
        stats = self.get_today_stats()
        print(f"今日已喝水：{stats['count']} 次")
        print(f"今日已提醒：{stats['reminded']} 次")
        print()

        while True:
            try:
                now = datetime.now()
                current_hour = now.hour
                current_minute = now.minute

                # 检查是否是提醒时间
                if self.is_reminder_time(current_hour, current_minute):
                    print(f"[{now.strftime('%H:%M:%S')}] 触发提醒")
                    self.show_reminder()
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
