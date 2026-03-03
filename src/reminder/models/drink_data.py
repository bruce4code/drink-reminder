#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型层 - 喝水数据管理
负责数据持久化、业务逻辑和数据操作
"""

import json
import os
import random
from datetime import datetime
from ..config import (
    DATA_FILE,
    DAILY_GOAL,
    HISTORY_DAYS
)


class DrinkData:
    """喝水数据管理类"""

    def __init__(self, data_file=None):
        """
        初始化数据模型

        Args:
            data_file: 数据文件路径，默认使用配置中的路径
        """
        self.data_file = data_file or DATA_FILE
        self.daily_goal = DAILY_GOAL
        self.history_days = HISTORY_DAYS

        # 确保数据文件在项目根目录
        if not os.path.isabs(self.data_file):
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            self.data_file = os.path.join(root_dir, self.data_file)

        self.data = None
        self.load_data()

    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = self._create_empty_data()
        else:
            self.data = self._create_empty_data()

        # 检查日期，如果是新的一天，重置数据
        today = datetime.now().strftime("%Y-%m-%d")
        if self.data.get("current_date") != today:
            self.reset_today(today)

    def _create_empty_data(self):
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
        """重置今日数据

        Args:
            today: 今天的日期字符串
        """
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

        # 只保留最近N天的历史
        if len(self.data["history"]) > self.history_days:
            dates = sorted(self.data["history"].keys())
            for old_date in dates[:-self.history_days]:
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
        return current_time, self.data["today"]["count"]

    def record_reminder(self):
        """记录提醒次数"""
        self.data["today"]["reminded"] += 1
        self.save_data()

    def get_progress(self):
        """获取进度百分比"""
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

        return random.choice(messages)

    def get_today_stats(self):
        """获取今日统计信息"""
        return {
            "count": self.data["today"]["count"],
            "reminded": self.data["today"]["reminded"],
            "times": self.data["today"]["times"],
            "goal": self.daily_goal,
            "progress": self.get_progress()
        }

    def get_history(self):
        """获取历史记录"""
        return self.data.get("history", {})
