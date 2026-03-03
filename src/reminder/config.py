#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
"""

# 提醒设置
REMINDER_START_TIME = "09:00"  # 提醒开始时间
REMINDER_END_TIME = "21:00"    # 提醒结束时间
REMINDER_INTERVAL = 3600        # 提醒间隔（秒）
SNOOZE_MINUTES = 5              # 稍后提醒时间（分钟）

# 目标设置
DAILY_GOAL = 8                  # 每日喝水目标（杯）

# 数据设置
DATA_FILE = "drink_data.json"   # 数据文件名
HISTORY_DAYS = 30               # 保留历史记录天数

# 日志设置
LOG_LEVEL = "INFO"               # 日志级别: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "reminder.log"        # 日志文件名
