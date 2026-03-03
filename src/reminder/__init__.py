# -*- coding: utf-8 -*-
"""
喝水提醒程序 - 智能提醒您定时喝水
"""

__version__ = "0.3.0"

# 导出主要类，方便外部使用
from .models import DrinkData
from .views import DrinkGUI
from .controllers import ReminderController
from .config import (
    REMINDER_START_TIME,
    REMINDER_END_TIME,
    REMINDER_INTERVAL,
    SNOOZE_MINUTES,
    DAILY_GOAL,
    DATA_FILE,
    HISTORY_DAYS,
    LOG_LEVEL,
    LOG_FILE
)
from .utils import get_logger

__all__ = [
    'DrinkData',
    'DrinkGUI',
    'ReminderController',
    'REMINDER_START_TIME',
    'REMINDER_END_TIME',
    'REMINDER_INTERVAL',
    'SNOOZE_MINUTES',
    'DAILY_GOAL',
    'DATA_FILE',
    'HISTORY_DAYS',
    'LOG_LEVEL',
    'LOG_FILE',
    'get_logger'
]
